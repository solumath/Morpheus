import discord
from discord.utils import get
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("BotPR")
    @commands.is_owner()
    async def role(self, ctx, phrase, room, max, *roles: discord.Role):
        opt = []
        channel = self.bot.get_channel(int(room[2:-1]))

        for role in roles:
            opt.append(create_select_option(f"{role.name}", value=role.id))

        select = create_select(
            options=opt,
            placeholder=phrase,
            min_values=1,
            max_values=max,
        )
        await channel.send(phrase, components=[create_actionrow(select)])

    @commands.Cog.listener()
    async def on_component(self, ctx):
        await ctx.defer(edit_origin=True)

        # All options from menu
        roles_options = set(map(lambda num : int(num["value"]), ctx.component["options"]))

        # User roles
        user = ctx.author
        user_has_roles = set(map(lambda role : role.id, user.roles))

        selected = set(map(int, ctx.selected_options))

        not_selected = roles_options - selected

        to_remove = set.intersection(not_selected, user_has_roles)
        to_add = selected - user_has_roles

        if to_add:
            for role_id in to_add:
                role = get(ctx.guild.roles, id=role_id)
                await user.add_roles(role)

        if to_remove:
            for role_id in to_remove:
                role = get(ctx.guild.roles, id=role_id)
                await user.remove_roles(role)

def setup(bot):
    bot.add_cog(Roles(bot))
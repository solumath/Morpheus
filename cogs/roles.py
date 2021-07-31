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
    async def role(self, ctx, max, phrase, *roles: discord.Role):
        opt = []

        for role in roles:
            opt.append(create_select_option(f"{role.name}", value=role.id))

        select = create_select(
            options=opt,
            placeholder=phrase,
            min_values=1,
            max_values=max,
        )

        await ctx.send(phrase, components=[create_actionrow(select)])

    @commands.Cog.listener()
    async def on_component(self, ctx):
        await ctx.defer(edit_origin=True)
        
        roles_options = []
        for num in ctx.component["options"]:
            roles_options.append(num["value"])
        roles_options = list(map(int, roles_options))           # all options from menu

        user: discord.Member = ctx.author
        user_has_roles = user.roles[1:]                         # all roles except @everyone user has
        selected = list(map(int, ctx.selected_options))

        difference = set(roles_options) - set(selected)

        for role_id in selected:
            role = get(ctx.guild.roles, id=role_id)
            await user.add_roles(role)
        
        if difference:
            for role_id in difference:
                role = get(ctx.guild.roles, id=role_id)
                await user.remove_roles(role)
        
        

def setup(bot):
    bot.add_cog(Roles(bot))
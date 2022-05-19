import disnake
from disnake.utils import get
from disnake.ext import commands
from config import channels

channels = channels.Channels

class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="select", description="Create select menu")
    async def select(self, ctx, room : disnake.TextChannel, text : str, 
                    min_roles : int, max_roles : int, roles: str):
        """extract roles from string and create select menu"""
        roles = roles.split()
        opt = []
        for role in roles:
            role = role[3:-1]
            opt.append(int(role))

        roles = []
        for id in opt:
            role = ctx.guild.get_role(id)
            roles.append(disnake.SelectOption(label=role.name, value=role.id))
        
        await ctx.send("select menu sent")
        await room.send(components=disnake.ui.Select(placeholder=text, min_values=min_roles, 
                                                     max_values=max_roles, options=roles, custom_id="role_select"))

    @commands.Cog.listener("on_dropdown")
    async def cool_select_listener(self, ctx: disnake.MessageInteraction):
        if ctx.component.custom_id != "role_select":
            return

        #All options from menu
        roles_options = set([int(o.value) for o in ctx.component.options])

        #User roles
        user = ctx.author
        user_has_roles = set(map(lambda role : role.id, user.roles))

        selected = set(map(int, ctx.values))

        not_selected = roles_options - selected

        to_remove = set.intersection(not_selected, user_has_roles)
        to_add = selected - user_has_roles

        selected = []
        if to_add:
            for role_id in to_add:
                role = get(ctx.guild.roles, id=role_id)
                selected.append(role)
                await user.add_roles(role)

        if to_remove:
            for role_id in to_remove:
                role = get(ctx.guild.roles, id=role_id)
                await user.remove_roles(role)

        selected = [role.mention for role in selected]
        await ctx.response.send_message(f"You selected {' '.join(selected)}.", ephemeral=True)

def setup(bot):
    bot.add_cog(Buttons(bot))

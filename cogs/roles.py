import disnake
from disnake.utils import get
from disnake.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="select", description="Create select menu")
    async def select(self, inter: disnake.ApplicationCommandInteraction, 
                    room : disnake.TextChannel, text : str, 
                    min_roles : int, max_roles : int, roles: str):
        """extract roles from string and create select menu"""
        roles = roles.split()
        opt = []
        for role in roles:
            role = role[3:-1]
            opt.append(int(role))

        roles = []
        for id in opt:
            role = inter.guild.get_role(id)
            roles.append(disnake.SelectOption(label=role.name, value=role.id))

        await inter.response.send_message("select menu sent")
        await room.send(components=disnake.ui.Select(placeholder=text, min_values=min_roles, 
                                                     max_values=max_roles, options=roles, custom_id="role_select"))

    @commands.Cog.listener("on_dropdown")
    async def cool_select_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id != "role_select":
            return

        #All options from menu
        roles_options = set([int(o.value) for o in inter.component.options])

        #User roles
        user = inter.author
        user_has_roles = set(map(lambda role : role.id, user.roles))

        selected = set(map(int, inter.values))

        not_selected = roles_options - selected

        to_remove = set.intersection(not_selected, user_has_roles)
        to_add = selected - user_has_roles

        selected = []
        if to_add:
            for role_id in to_add:
                role = get(inter.guild.roles, id=role_id)
                selected.append(role)
                await user.add_roles(role)

        if to_remove:
            for role_id in to_remove:
                role = get(inter.guild.roles, id=role_id)
                await user.remove_roles(role)

        selected = [role.mention for role in selected]
        await inter.response.send_message(f"You selected {' '.join(selected)}.", ephemeral=True)


def setup(bot):
    bot.add_cog(Roles(bot))

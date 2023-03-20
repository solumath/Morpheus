import disnake
from disnake.ext import commands
from disnake.utils import get

import utility


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(utility.is_bot_admin)
    @commands.slash_command(name="select", description="Create role select menu")
    async def select(self, inter: disnake.ApplicationCommandInteraction,
                     placeholder: str, roles: str,
                     min_roles: int, max_roles: int):
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

        await inter.send(
            components=disnake.ui.StringSelect(
                placeholder=placeholder,
                min_values=min_roles,
                max_values=max_roles,
                options=roles,
                custom_id="role:select"
            )
        )

    @commands.check(utility.is_bot_admin)
    @commands.slash_command(name="rooms", description="Create select menu for rooms")
    async def rooms(
                    self,
                    inter: disnake.ApplicationCommandInteraction,
                    category: disnake.CategoryChannel,
                    placeholder: str,
                    ):
        """extract all channels from category for permission overwrite"""

        await inter.send(
            components=disnake.ui.StringSelect(
                placeholder=placeholder,
                min_values=0,
                max_values=len(category.channels),
                options=[
                    disnake.SelectOption(
                        label=channel.name,
                        value=channel.id
                    ) for channel in category.channels
                ],
                custom_id="channel:select"
            )
        )

    @commands.Cog.listener("on_dropdown")
    async def cool_select_listener(self, inter: disnake.MessageInteraction):
        await inter.response.defer()
        if inter.component.custom_id == "channel:select":
            channel_options = set([int(o.value) for o in inter.component.options])

            # No channel selected
            if inter.values is None:
                for channel_id in channel_options:
                    channel = self.bot.get_channel(int(channel_id))
                    await channel.set_permissions(inter.author, view_channel=False)
                await inter.send("All channels removed.", ephemeral=True)
                return

            selected = set(map(int, inter.values))
            to_remove = channel_options - selected

            channels = []
            for channel_id in inter.values:
                channel = self.bot.get_channel(int(channel_id))
                channels.append(channel)
                await channel.set_permissions(inter.author, view_channel=True)

            for channel_id in to_remove:
                channel = self.bot.get_channel(int(channel_id))
                await channel.set_permissions(inter.author, view_channel=False)

            await inter.send(
                f"You selected {' '.join([channel.mention for channel in channels])}.", ephemeral=True)

        elif inter.component.custom_id == "role:select":
            # All options from menu
            roles_options = set([int(o.value) for o in inter.component.options])

            # User roles
            user = inter.author
            user_has_roles = set(map(lambda role: role.id, user.roles))

            # No roles selected
            if inter.values is None:
                for role_id in roles_options:
                    role = get(inter.guild.roles, id=role_id)
                    await user.remove_roles(role)
                await inter.send("All roles removed.", ephemeral=True)
                return

            # Selected roles
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
            await inter.send(f"You selected {' '.join(selected)}.", ephemeral=True)

        else:
            pass


def setup(bot):
    bot.add_cog(Roles(bot))

import discord
from discord.ext import commands
from discord.utils import get


class RolesSelectView(discord.ui.View):
    """Parameters are none so the view can be persistent"""

    def __init__(
        self,
        bot: commands.Bot,
        roles: list = None,
        placeholder: str = "Select role(s)",
        min_roles: int = 0,
        max_roles: int = 1,
    ):
        super().__init__(timeout=None)

        self.add_item(RoleSelect(bot, roles, placeholder, min_roles, max_roles))


class RoleSelect(discord.ui.Select):
    def __init__(
        self,
        bot: commands.Bot,
        roles: list = None,
        placeholder: str = "Select role(s)",
        min_roles: int = 0,
        max_roles: int = 1,
    ):
        self.bot = bot
        options = []
        if roles:
            options = [discord.SelectOption(label=role.name, value=role.id) for role in roles]

        super().__init__(
            placeholder=placeholder,
            min_values=min_roles,
            max_values=max_roles,
            options=options,
            custom_id="role:select",
        )

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer()

        # All options from select
        options = inter.message.components[0].children[0].options
        roles_options = set([int(role.value) for role in options])

        # User roles
        user_has_roles = set(map(lambda role: role.id, inter.user.roles))

        # selected values
        values = inter.data.get("values", None)
        # No roles selected
        if values is None:
            for role_id in roles_options:
                role = get(inter.guild.roles, id=role_id)
                await inter.user.remove_roles(role)
            await inter.followup.send("All roles removed.", ephemeral=True)
            return

        # Selected roles
        selected = set(map(int, values))

        not_selected = roles_options - selected

        to_remove = set.intersection(not_selected, user_has_roles)
        to_add = selected - user_has_roles

        selected = []
        if to_add:
            for role_id in to_add:
                role = get(inter.guild.roles, id=role_id)
                selected.append(role)
                await inter.user.add_roles(role)

        if to_remove:
            for role_id in to_remove:
                role = get(inter.guild.roles, id=role_id)
                await inter.user.remove_roles(role)

        selected = [role.mention for role in selected]
        await inter.followup.send(f"You selected {' '.join(selected)}.", ephemeral=True)


class ChannelsSelectView(discord.ui.View):
    """Parameters are none so the view can be persistent"""

    def __init__(
        self,
        bot: commands.Bot,
        category: discord.CategoryChannel = None,
        placeholder: str = "Select channel(s)",
        min_channels: int = 0,
        max_channels: int = 1,
    ):
        super().__init__(timeout=None)

        self.add_item(ChannelsSelect(bot, category, placeholder, min_channels, max_channels))


class ChannelsSelect(discord.ui.Select):
    def __init__(
        self,
        bot: commands.Bot,
        category: discord.CategoryChannel = None,
        placeholder: str = "Select channel(s)",
        min_channels: int = 0,
        max_channels: int = 1,
    ):
        self.bot = bot
        options = []
        if category:
            options = [discord.SelectOption(label=channel.name, value=channel.id) for channel in category.channels]

        super().__init__(
            placeholder=placeholder,
            min_values=min_channels,
            max_values=max_channels,
            options=options,
            custom_id="channel:select",
        )

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer()
        options = inter.message.components[0].children[0].options
        channel_options = set([int(channel.value) for channel in options])

        # selected values
        values = inter.data.get("values", None)
        # No channel selected
        if values is None:
            for channel_id in channel_options:
                channel = self.bot.get_channel(int(channel_id))
                await channel.set_permissions(inter.user, view_channel=False)
            await inter.followup.send("All channels removed.", ephemeral=True)
            return

        selected = set(map(int, values))
        to_remove = channel_options - selected

        channels = []
        for channel_id in values:
            channel = self.bot.get_channel(int(channel_id))
            channels.append(channel)
            await channel.set_permissions(inter.user, view_channel=True)

        for channel_id in to_remove:
            channel = self.bot.get_channel(int(channel_id))
            await channel.set_permissions(inter.user, view_channel=False)

        await inter.followup.send(
            f"You selected {' '.join([channel.mention for channel in channels])}.", ephemeral=True
        )

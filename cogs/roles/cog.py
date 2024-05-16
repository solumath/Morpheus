from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from cogs.base import Base
from custom.permission_check import is_bot_admin

from .dropdowns import ChannelsSelectView, RolesSelectView
from .messages import RolesMess

if TYPE_CHECKING:
    from morpheus import Morpheus


class Roles(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def init_views(self):
        """Add permanent views to the bot"""
        self.bot.add_view(RolesSelectView(self.bot))
        self.bot.add_view(ChannelsSelectView(self.bot))

    @app_commands.check(is_bot_admin)
    @app_commands.command(name="roles_select", description=RolesMess.role_select_brief)
    async def roles_select(
        self, inter: discord.Interaction, placeholder: str, roles: str, min_roles: int, max_roles: int
    ):
        """extract roles from string and create select menu"""
        roles = roles.split()
        options = []
        for role in roles:
            role_id = role[3:-1]
            role = inter.guild.get_role(int(role_id))
            options.append(role)

        view = RolesSelectView(self.bot, options, placeholder, min_roles, max_roles)

        await inter.response.send_message(view=view)

    @app_commands.check(is_bot_admin)
    @app_commands.command(name="channels_select", description=RolesMess.channel_select_brief)
    async def channels_select(
        self,
        inter: discord.Interaction,
        category: discord.CategoryChannel,
        placeholder: str,
    ):
        """extract all channels from category for permission overwrite"""

        view = ChannelsSelectView(self.bot, category, placeholder, 0, len(category.channels))

        await inter.response.send_message(view=view)

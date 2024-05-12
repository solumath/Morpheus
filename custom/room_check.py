from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from config.app_config import config

if TYPE_CHECKING:
    from morpheus import Morpheus


class RoomCheck:
    def __init__(self, bot: Morpheus):
        self.bot = bot

    def botroom_check(self, inter: discord.Interaction) -> bool:
        """Checks if the interaction is in a bot channel.

        Used for ephemeral commands.

        Returns
        --------
        `bool`
            False (in DMs with bot, in thread, in allowed channel) else True
        """

        # DMs with bot
        if inter.guild is None:
            return False

        # allow threads in channels
        if isinstance(inter.channel, discord.Thread):
            return False

        # allowed channels
        if inter.channel_id in config.allowed_channels:
            return False

        return True

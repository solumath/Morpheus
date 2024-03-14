from enum import Enum
from typing import Any, Union

import discord
from discord.ext import commands


class DiscordTimestamps(Enum):
    """
    Default and Short Date/Time formats are identical, but for the sake of consistency,
    I've left them as separate options.
    """

    Default = ""  # 28 November 2018 09:01
    ShortTime = "t"  # 09:01
    LongTime = "T"  # 09:01:00
    ShortDate = "d"  # 28/11/2018
    LongDate = "D"  # 28 November 2018
    ShortDateTime = "f"  # 28 November 2018 09:01
    LongDateTime = "F"  # Wednesday, 28 November 2018 09:01
    RelativeTime = "R"  # 3 years ago


class CooldownType(Enum):
    """
    This is a copy of the CooldownType enum from discord.ext.commands with edit for app_commands
    """

    default = 0
    user = 1
    guild = 2
    channel = 3
    member = 4
    category = 5
    role = 6

    def get_key(self, msg: Union[discord.Message, commands.Context[Any], discord.Interaction]) -> Any:
        author = msg.user if isinstance(msg, discord.Interaction) else msg.author

        if self is CooldownType.user:
            return author.id
        elif self is CooldownType.guild:
            return (msg.guild or author).id
        elif self is CooldownType.channel:
            return msg.channel.id
        elif self is CooldownType.member:
            return ((msg.guild and msg.guild.id), author.id)
        elif self is CooldownType.category:
            return (msg.channel.category or msg.channel).id  # type: ignore
        elif self is CooldownType.role:
            # we return the channel id of a private-channel as there are only roles in guilds
            # and that yields the same result as for a guild with only the @everyone role
            # NOTE: PrivateChannel doesn't actually have an id attribute but we assume we are
            # receiving a DMChannel or GroupChannel which inherit from PrivateChannel and do
            id = (msg.channel if isinstance(msg.channel, discord.abc.PrivateChannel) else author.top_role).id
            return id

    def __call__(self, msg: Union[discord.Message, commands.Context[Any], discord.Interaction]) -> Any:
        return self.get_key(msg)

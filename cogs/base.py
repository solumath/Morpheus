"""
Base cog class. All cogs should inherit from this class.
"""

from functools import cached_property

import discord

from config.app_config import config, load_config


class Base:
    config = config

    def __init__(self):
        self.tasks = []
        self.permanent_views = []

    @cached_property
    def base_guild(self) -> discord.TextChannel:
        return self.bot.get_guild(Base.config.guild_id)

    @cached_property
    def bot_channel(self) -> discord.TextChannel:
        return self.bot.get_channel(self.config.bot_channel)

    @cached_property
    def bot_dev_channel(self) -> discord.TextChannel:
        return self.bot.get_channel(self.config.bot_dev_channel)

    @cached_property
    def name_day_channel(self) -> discord.TextChannel:
        return self.bot.get_channel(self.config.name_day_channel)

    @cached_property
    def gay_channel(self) -> discord.TextChannel:
        return self.bot.get_channel(self.config.gay_channel)

    def cog_unload(self) -> None:
        for task in self.tasks:
            task.cancel()

    def cog_load(self) -> None:
        load_config()
        for view in self.permanent_views:
            self.bot.add_view(view(self.bot))

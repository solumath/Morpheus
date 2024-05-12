from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

from cogs.base import Base
from config.app_config import config

if TYPE_CHECKING:
    from morpheus import Morpheus


class Threads(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def create_thread(self, ctx):
        for room in config.threads_with_reaction:
            if ctx.channel.id == room:
                await ctx.create_thread(name="Rename me", auto_archive_duration=1440)
                await ctx.add_reaction(str("✅"))
                await ctx.add_reaction(str("❌"))
        for room in config.thread_channels:
            if ctx.channel.id == room:
                await ctx.create_thread(name="Rename me", auto_archive_duration=1440)

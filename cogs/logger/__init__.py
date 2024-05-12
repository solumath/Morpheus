from __future__ import annotations

from typing import TYPE_CHECKING

from .cog import Logger
from .levels import LoggerLeveles
from .top_logger import top_logger

if TYPE_CHECKING:
    from morpheus import Morpheus


async def setup(bot: Morpheus):
    LoggerLeveles.add_level_names()
    await bot.add_cog(Logger(bot))


def teardown(_):
    top_logger.guild_loggers.clear()

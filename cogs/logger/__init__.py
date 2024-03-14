from discord.ext import commands

from .cog import Logger
from .levels import LoggerLeveles
from .top_logger import top_logger


async def setup(bot: commands.Bot):
    LoggerLeveles.add_level_names()
    await bot.add_cog(Logger(bot))


def teardown(_):
    top_logger.guild_loggers.clear()

from discord.ext import commands

from .cog import Threads


async def setup(bot: commands.Bot):
    await bot.add_cog(Threads(bot))

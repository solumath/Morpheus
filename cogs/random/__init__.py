from discord.ext import commands

from .cog import Random


async def setup(bot: commands.Bot):
    await bot.add_cog(Random(bot))

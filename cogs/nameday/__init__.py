from discord.ext import commands

from .cog import NameDay


async def setup(bot: commands.Bot):
    await bot.add_cog(NameDay(bot))

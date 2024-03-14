from discord.ext import commands

from .cog import Weather


async def setup(bot: commands.Bot):
    await bot.add_cog(Weather(bot))

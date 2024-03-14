from discord.ext import commands

from .cog import Restaurants


async def setup(bot: commands.Bot):
    await bot.add_cog(Restaurants(bot))

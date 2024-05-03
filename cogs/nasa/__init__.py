from discord.ext import commands

from .cog import Nasa


async def setup(bot: commands.Bot):
    await bot.add_cog(Nasa(bot))

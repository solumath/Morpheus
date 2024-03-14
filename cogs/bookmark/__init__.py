from discord.ext import commands

from .cog import Bookmark


async def setup(bot: commands.Bot):
    await bot.add_cog(Bookmark(bot))

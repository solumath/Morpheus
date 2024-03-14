from discord.ext import commands

from .cog import Gay


async def setup(bot: commands.Bot):
    await bot.add_cog(Gay(bot))

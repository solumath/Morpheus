from discord.ext import commands

from .cog import Error


async def setup(bot: commands.Bot):
    await bot.add_cog(Error(bot))

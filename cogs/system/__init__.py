from discord.ext import commands

from .cog import System


async def setup(bot: commands.Bot):
    await bot.add_cog(System(bot))

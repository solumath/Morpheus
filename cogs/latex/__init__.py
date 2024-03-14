from discord.ext import commands

from .cog import Latex


async def setup(bot: commands.Bot):
    await bot.add_cog(Latex(bot))

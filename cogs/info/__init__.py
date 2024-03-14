from discord.ext import commands

from .cog import Info


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))

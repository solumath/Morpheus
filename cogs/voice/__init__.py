from discord.ext import commands

from .cog import Voice


async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))

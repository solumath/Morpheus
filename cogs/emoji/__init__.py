from discord.ext import commands

from .cog import Emoji


async def setup(bot: commands.Bot):
    await bot.add_cog(Emoji(bot))

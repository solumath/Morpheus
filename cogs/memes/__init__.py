from discord.ext import commands

from .cog import Memes


async def setup(bot: commands.Bot):
    await bot.add_cog(Memes(bot))

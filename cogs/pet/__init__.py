from discord.ext import commands

from .cog import Pet


async def setup(bot: commands.Bot):
    await bot.add_cog(Pet(bot))

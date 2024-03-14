from discord.ext import commands

from .cog import Roles


async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))

from discord.ext import commands

from .cog import GuildConfig


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildConfig(bot))

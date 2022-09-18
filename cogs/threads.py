from disnake.ext import commands
from config.app_config import config


class Threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def create(self, ctx):
        for room in config.thread_with_reaction:
            if ctx.channel.id == room:
                await ctx.create_thread(name="Rename me", auto_archive_duration=1440)
                await ctx.add_reaction(str("✅"))
                await ctx.add_reaction(str("❌"))
        for room in config.thread_room:
            if ctx.channel.id == room:
                await ctx.create_thread(name="Rename me", auto_archive_duration=1440)


def setup(bot):
    bot.add_cog(Threads(bot))

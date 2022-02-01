import disnake
from disnake.ext import commands

import env

class Threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener("on_message")
    async def create(self, ctx):
        if ctx.channel.id == env.plans:
            await ctx.add_reaction(str("✅"))
            await ctx.add_reaction(str("❌"))
            await ctx.create_thread(name="Rename me", auto_archive_duration=1440)

def setup(bot):
    bot.add_cog(Threads(bot))

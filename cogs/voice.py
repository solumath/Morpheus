import discord
from discord.ext import commands
from discord_slash import cog_ext

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="join")
    async def join(self, ctx):
        if not ctx.author.voice.channel:
            await ctx.send("Musíš být v hovoru")
            return
        else:
            channel = ctx.author.voice.channel
        await channel.connect()
    
    @cog_ext.cog_slash(name="leave")
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    #TODO

def setup(bot):
    bot.add_cog(Voice(bot))
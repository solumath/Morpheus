import discord
from discord.ext import commands

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True,aliases=["j"])
    async def join(self, ctx):
        if not ctx.author.voice.channel:
            await ctx.send("Musíš být v hovoru")
            return
        else:
            channel = ctx.author.voice.channel
        await channel.connect()
    
    @commands.command(pass_context=True,aliases=["l"])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    #TODO

def setup(bot):
    bot.add_cog(Voice(bot))
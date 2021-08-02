import discord
from discord.ext import commands
from discord_slash import cog_ext

import aiohttp
import random
import asyncio
import env

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="drzpicu", description="Drz picu 'user'")
    async def drzpicu(self, ctx, user = "<@153480398054227978>"):
        await ctx.send(f"drz picu {user}")

    @cog_ext.cog_slash(name="nebudsalty", description="Nebud salty 'user'")
    async def nebudsalty(self, ctx, user = "<@624604891603795968>"):
        await ctx.send(f":salt: nebud salty {user}")
    
    @commands.cooldown(rate=1, per=100.0, type=commands.BucketType.user)
    @commands.command()
    async def tagrage(self, ctx, user: discord.Member, *text):
        await ctx.message.delete()
        for x in range(5):
            await ctx.send(f"{user.mention} {' '.join(text)}")
            await asyncio.sleep(15)
    
    @tagrage.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            msg = 'Dostal jsi cooldown {:.2f}s'.format(error.retry_after)
            await ctx.send(msg)
        else:
            raise error

def setup(bot):
    bot.add_cog(Memes(bot))

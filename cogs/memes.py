import discord
from discord.ext import commands
from discord_slash import cog_ext

import aiohttp
import random

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="drzpicu", description="Drz picu soti")
    async def drzpicu(self, ctx, user = "<@153480398054227978>"):
        await ctx.send(f"drz picu {user}")

def setup(bot):
    bot.add_cog(Memes(bot))
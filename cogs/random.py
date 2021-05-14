import discord
from discord.ext import commands
from discord_slash import cog_ext

import random

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="flip", description="flip a coin")
    async def flip(self, ctx):
        await ctx.send(random.randint(0, 1))

    @cog_ext.cog_slash(name="roll", description="Roll a dice for range")
    async def roll(self, ctx, x : int, y : int = 0):
        if x > y:
            x, y = y, x
        await ctx.send(str(random.randint(x, y)))

    @cog_ext.cog_slash(name="pick", description="Pick a random thing")
    async def pick(self, ctx, arg1 : str, arg2 : str, arg3 : str = None, arg4 : str = None,
                    arg5 : str = None, arg6 : str = None, arg7 : str = None,
                    arg8 : str = None, arg9 : str = None, arg10 : str = None):
        
        # for now works
        args = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
        choices = [i for i in args if i]
        rng = random.choice(choices)
        await ctx.send(rng)
    
def setup(bot):
    bot.add_cog(Random(bot))
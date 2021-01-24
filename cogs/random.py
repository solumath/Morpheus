import discord
import random
from discord.ext import commands

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["coinflip", "coin"])
    async def flip(self, ctx):
        """Flip a coin"""
        await ctx.send(random.randint(0, 1))

    @commands.command(aliases=["rng", "random"], usage = "roll x (y) numbers must be integers")
    async def roll(self, ctx, x : int, y : int = 0):
        """Roll a dice for range ?roll x (y)"""
        if x > y:
            x, y = y, x
        await ctx.send(str(random.randint(x, y)))

    @roll.error
    async def command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send(ctx.command.usage)

def setup(bot):
    bot.add_cog(Random(bot))
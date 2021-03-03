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

    @commands.command(aliases=["rng", "random"], usage = "roll x (y) musí být celá čísla")
    async def roll(self, ctx, x : int, y : int = 0):
        """Roll a dice for range ?roll x (y)"""
        if x > y:
            x, y = y, x
        await ctx.send(str(random.randint(x, y)))

    @commands.command(usage = "?pick x y ...")
    async def pick(self, ctx, *args):
        """pick a random argument"""
        for i, arg in enumerate(args):
            if "?" in arg:
                args = args[i + 1:]
                break
        if not len(args):
            await ctx.send(f"nejsem fcking vědma, abych vařil z vody <:Reee:747845163279319180> {ctx.author.mention}") 

        choice = discord.utils.escape_mentions(random.choice(args))
        if choice:
            await ctx.send(f"{choice} {ctx.author.mention}")
    
    @pick.error
    @roll.error
    async def command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send(f"{ctx.command.usage} {ctx.author.mention}")

def setup(bot):
    bot.add_cog(Random(bot))
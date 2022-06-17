import disnake
from disnake.ext import commands

import random

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="flip", description="flip a coin")
    async def flip(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(random.randint(0, 1))

    @commands.slash_command(name="roll", description="Roll a dice for range")
    async def roll(self, inter: disnake.ApplicationCommandInteraction, x : int, y : int = 0):
        if x > y:
            x, y = y, x
        await inter.response.send_message(str(random.randint(x, y)))

    @commands.slash_command(name="pick", description="Pick a random thing")
    async def pick(self, inter: disnake.ApplicationCommandInteraction, 
                   arg1 : str, arg2 : str, arg3 : str = None, arg4 : str = None,
                   arg5 : str = None, arg6 : str = None, arg7 : str = None,
                   arg8 : str = None, arg9 : str = None, arg10 : str = None):

        # for now works
        args = [arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10]
        choices = [i for i in args if i]
        rng = random.choice(choices)
        await inter.response.send_message(rng)


def setup(bot):
    bot.add_cog(Random(bot))

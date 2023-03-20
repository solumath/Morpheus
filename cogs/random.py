import random
import shlex

import disnake
from disnake.ext import commands


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="flip", description="flip a coin")
    async def flip(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(random.randint(0, 1))

    @commands.slash_command(name="roll", description="Roll a dice for range")
    async def roll(self, inter: disnake.ApplicationCommandInteraction, x: int, y: int = 0):
        if x > y:
            x, y = y, x
        await inter.response.send_message(str(random.randint(x, y)))

    @commands.slash_command(name="pick", description="Pick a random thing")
    async def pick(
        self,
        inter: disnake.ApplicationCommandInteraction,
        args: str = commands.Param(max_length=1900)
    ):
        args = shlex.split(args)

        option = disnake.utils.escape_mentions(random.choice(args))
        await inter.send(f"{option[:1900]} {inter.author.mention}")


def setup(bot):
    bot.add_cog(Random(bot))

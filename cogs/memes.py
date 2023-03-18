import disnake
from disnake.ext import commands
from config.app_config import config

import asyncio


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jany = bot.get_user(config.jany)
        self.ilbinek = bot.get_user(config.ilbinek)

    @commands.slash_command(name="drzpicu", description="Drz picu 'user'")
    async def drzpicu(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        if user is None:
            user = self.ilbinek
        await inter.send(f"drz picu {user.mention}")

    @commands.slash_command(name="nebudsalty", description="Nebud salty 'user'")
    async def nebudsalty(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        if user is None:
            user = self.jany
        await inter.send(f":salt: nebud salty {user.mention}")

    @commands.cooldown(rate=1, per=100.0, type=commands.BucketType.user)
    @commands.command()
    async def tagrage(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member, *text):
        await inter.message.delete()
        for x in range(5):
            await inter.send(f"{user.mention} {' '.join(text)}")
            await asyncio.sleep(5)

    @commands.slash_command(name="nickname", description="Change nickname")
    async def nick(self, inter: disnake.ApplicationCommandInteraction, nickname, target: disnake.Member):
        accept = len(nickname)
        if accept > 32:
            await inter.send("Nickname must be 32 characters or less")
        else:
            try:
                await target.edit(nick=nickname)
            except disnake.errors.Forbidden:
                await inter.send("Cant change this ones name")
            else:
                await inter.send("Nickname has been changed.")


def setup(bot):
    bot.add_cog(Memes(bot))

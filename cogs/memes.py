import disnake
from disnake.ext import commands
from typing import Dict

import re
import aiohttp
import random
import asyncio


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ilbinek = bot.get_user(153480398054227978)
        self.jany = bot.get_user(624604891603795968)
    
    @commands.slash_command(name="drzpicu", description="Drz picu 'user'")
    async def drzpicu(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User=None):
        if user is None:
            user = self.ilbinek
        await inter.send(f"drz picu {user.mention}")

    @commands.slash_command(name="nebudsalty", description="Nebud salty 'user'")
    async def nebudsalty(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User=None):
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

    @commands.slash_command(name="dadjoke", description="Get a dadjoke")
    async def dadjoke(self, inter: disnake.ApplicationCommandInteraction, *, keyword=None):
        """Get random dad joke
        Arguments
        ---------
        keyword: search for a certain keyword in a joke
        """
        if keyword is not None and ("&" in keyword or "?" in keyword):
            await inter.send("I didn't find a joke like that.")

        params: Dict[str, str] = {"limit": "30"}
        url: str = "https://icanhazdadjoke.com"
        if keyword is not None:
            params["term"] = keyword
            url += "/search"
        headers: Dict[str, str] = {"Accept": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                fetched = await response.json()

        if keyword is not None:
            res = fetched["results"]
            if len(res) == 0:
                await inter.send("I didn't find a joke like that.")
            result = random.choice(res)
            result["joke"] = re.sub(
                f"(\\b\\w*{keyword}\\w*\\b)",
                r"**\1**",
                result["joke"],
                flags=re.IGNORECASE,
            )
        else:
            result = fetched

        embed = disnake.Embed(description=result["joke"])

        await inter.send(embed=embed)

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

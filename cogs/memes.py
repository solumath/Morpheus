import disnake
from disnake.ext import commands

from typing import Dict

import re
import aiohttp
import random
import asyncio
import env

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="drzpicu", description="Drz picu 'user'")
    async def drzpicu(self, ctx, user = "<@153480398054227978>"):
        await ctx.send(f"drz picu {user}")

    @commands.slash_command(name="nebudsalty", description="Nebud salty 'user'")
    async def nebudsalty(self, ctx, user = "<@624604891603795968>"):
        await ctx.send(f":salt: nebud salty {user}")
    
    @commands.cooldown(rate=1, per=100.0, type=commands.BucketType.user)
    @commands.command()
    async def tagrage(self, ctx, user: disnake.Member, *text):
        await ctx.message.delete()
        for x in range(5):
            await ctx.send(f"{user.mention} {' '.join(text)}")
            await asyncio.sleep(15)
    
    @commands.slash_command(name="dadjoke", description="Get a dadjoke")
    async def dadjoke(self, ctx, *, keyword = None):
        """Get random dad joke
        Arguments
        ---------
        keyword: search for a certain keyword in a joke
        """
        if keyword is not None and ("&" in keyword or "?" in keyword):
            await ctx.send("I didn't find a joke like that.")

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
                await ctx.send("I didn't find a joke like that.")
            result = random.choice(res)
            result["joke"] = re.sub(
                f"(\\b\\w*{keyword}\\w*\\b)",
                r"**\1**",
                result["joke"],
                flags=re.IGNORECASE,
            )
        else:
            result = fetched

        embed = disnake.Embed(
            author=ctx.author,
            description=result["joke"],
            footer="icanhazdadjoke.com",
            url="https://icanhazdadjoke.com/j/" + result["id"],
        )

        await ctx.send(embed=embed)

    @commands.slash_command(name="nickname", description="Change nickname")
    async def nick(self, ctx, nickname, target: disnake.Member):
        accept = len(nickname)
        if accept > 32:
            await ctx.send("Nickname must be 32 characters or less")
        else:
            try:
                await target.edit(nick=nickname)
            except disnake.errors.Forbidden:
                await ctx.send("Cant change this ones name")
            else:
                await ctx.send("Nickname has been changed.")
    
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

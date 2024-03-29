"""
Cog containing commands that call random APIs for fun things.
"""

import contextlib
import random
import re
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional, Tuple

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from cogs.base import Base
from custom.cooldowns import default_cooldown
from custom.custom_errors import ApiError

from .messages import FunMess


class Fun(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    def custom_footer(self, author, url) -> str:
        return f"📩 {author} | {url} • {datetime.now().strftime('%d.%m.%Y %H:%M')}"

    async def get_image(self, inter, url) -> Optional[Tuple[BytesIO, str]]:
        async with aiohttp.ClientSession() as session:
            # get random image url
            async with session.get(url) as response:
                if response.status != 200:
                    raise ApiError(response.status)
                image = await response.json()

            # get image url
            if isinstance(image, list):
                url = image[0]["url"]
            else:
                url = image.get("url")
                if not url:
                    url = image.get("image")

            # get image bytes
            async with session.get(url) as response:
                if response.status != 200:
                    raise ApiError(response.status)
                file_name = url.split("/")[-1]
                return BytesIO(await response.read()), file_name

    async def get_fact(self, url, key) -> str:
        async with aiohttp.ClientSession() as session:
            with contextlib.suppress(OSError):
                async with session.get(url) as response:
                    if response.status == 200:
                        fact_response_ = await response.json()
                        fact_response = fact_response_[key][0]
        return fact_response

    @default_cooldown()
    @app_commands.command(name="cat", description=FunMess.cat_brief)
    async def cat(self, inter: discord.Interaction, breed: str = None):
        """Get random image of a cat"""
        image_bytes, file_name = await self.get_image(inter, "https://api.thecatapi.com/v1/images/search")
        image_file = discord.File(image_bytes, filename=file_name)

        fact_response: str = ""
        if random.randint(0, 9) == 1:
            fact_response = await self.get_fact("https://meowfacts.herokuapp.com/", "data")

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_footer(text=self.custom_footer(inter.user, "thecatapi.com"))
        embed.set_image(url=f"attachment://{file_name}")
        embeds: List[discord.Embed] = [embed]

        if fact_response:
            fact_embed = discord.Embed(
                title="Cat fact",
                description=fact_response,
                color=discord.Color.blue(),
            )
            fact_embed.set_footer(text=self.custom_footer(inter.user, "thecatapi.com"))
            embeds.append(fact_embed)

        await inter.response.send_message(file=image_file, embeds=embeds)

    @default_cooldown()
    @app_commands.command(name="dog", description=FunMess.dog_brief)
    async def dog(self, inter: discord.Interaction):
        """Get random image of a dog"""
        image_bytes, file_name = await self.get_image(inter, "https://api.thedogapi.com/v1/images/search")
        image_file = discord.File(image_bytes, filename=file_name)

        fact_response: str = ""
        if random.randint(0, 9) == 1:
            fact_response = await self.get_fact("https://dogapi.dog/api/facts/", "facts")

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_footer(text=self.custom_footer(inter.user, "thedogapi.com"))
        embed.set_image(url=f"attachment://{file_name}")
        embeds: List[discord.Embed] = [embed]

        if fact_response:
            fact_embed = discord.Embed(
                title="Dog fact",
                description=fact_response,
                color=discord.Color.blue(),
            )
            fact_embed.set_footer(text=self.custom_footer(inter.user, "thedogapi.com"))
            embeds.append(fact_embed)

        await inter.response.send_message(file=image_file, embeds=embeds)

    @default_cooldown()
    @app_commands.command(name="fox", description=FunMess.fox_brief)
    async def fox(self, inter: discord.Interaction):
        """Get random image of a fox"""
        image_bytes, file_name = await self.get_image(inter, "https://randomfox.ca/floof/")
        image_file = discord.File(image_bytes, filename=file_name)

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_footer(text=self.custom_footer(inter.user, "randomfox.ca"))
        embed.set_image(url=f"attachment://{file_name}")

        await inter.response.send_message(file=image_file, embed=embed)

    @default_cooldown()
    @app_commands.command(name="duck", description=FunMess.duck_brief)
    async def duck(self, inter: discord.Interaction):
        """Get random image of a duck"""
        image_bytes, file_name = await self.get_image(inter, "https://random-d.uk/api/v2/random")
        image_file = discord.File(image_bytes, filename=file_name)

        embed = discord.Embed(color=discord.Color.blue())
        embed.set_footer(text=self.custom_footer(inter.user, "random-d.uk"))
        embed.set_image(url=f"attachment://{file_name}")

        await inter.response.send_message(file=image_file, embed=embed)

    @default_cooldown()
    @app_commands.command(name="dadjoke", description=FunMess.dadjoke_brief)
    async def dadjoke(self, inter: discord.Interaction, keyword: str = None):
        """Get random dad joke
        Arguments
        ---------
        keyword: search for a certain keyword in a joke
        """
        if keyword is not None and ("&" in keyword or "?" in keyword):
            await inter.send("I didn't find a joke like that.")
            return

        params: Dict[str, str] = {"limit": "30"}
        url: str = "https://icanhazdadjoke.com"
        if keyword is not None:
            params["term"] = keyword
            url += "/search"
        headers: Dict[str, str] = {"Accept": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    raise ApiError(response.status)
                fetched = await response.json()

        if keyword is not None:
            res = fetched["results"]
            if len(res) == 0:
                await inter.send("I didn't find a joke like that.")
                return
            result = random.choice(res)
            result["joke"] = re.sub(
                f"(\\b\\w*{keyword}\\w*\\b)",
                r"**\1**",
                result["joke"],
                flags=re.IGNORECASE,
            )
        else:
            result = fetched

        embed = discord.Embed(
            title="Dadjoke",
            description=result["joke"],
            color=discord.Color.blue(),
            url="https://icanhazdadjoke.com/j/" + result["id"],
        )
        embed.set_footer(text=self.custom_footer(inter.user, "icanhazdadjoke.com"))

        await inter.response.send_message(embed=embed)

    @default_cooldown()
    @app_commands.command(name="yo_mamajoke", description=FunMess.yo_mamajoke_brief)
    async def yo_mamajoke(self, inter: discord.Interaction):
        """Get random Yo momma joke"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.yomomma.info/") as response:
                if response.status != 200:
                    raise ApiError(response.status)
                result = await response.json()

        embed = discord.Embed(
            title="Yo mamajoke",
            description=result["joke"],
            color=discord.Color.blue(),
            url="https://yomomma.info",
        )
        embed.set_footer(text=self.custom_footer(inter.user, "yomomma.info"))

        await inter.response.send_message(embed=embed)

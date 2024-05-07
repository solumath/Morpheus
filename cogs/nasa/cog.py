"""
Cog for sending name days and birthdays.
"""

import asyncio
from datetime import time

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

import utils.utils as utils
from cogs.base import Base
from custom import room_check
from custom.cooldowns import default_cooldown

from .features import create_nasa_embed
from .messages import NasaMess


class Nasa(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.tasks = [self.send_nasa_image.start()]
        self.check = room_check.RoomCheck(bot)

    async def nasa_daily_image(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                url = f"https://api.nasa.gov/planetary/apod?api_key={self.config.nasa_key}&concept_tags=True"
                async with session.get(url) as resp:
                    response = await resp.json()
                return response
            except (asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError):
                return "Website unreachable"

    @default_cooldown()
    @app_commands.command(name="nasa_daily_image", description=NasaMess.nasa_image_brief)
    async def nasa_image(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=self.check.botroom_check(inter))
        response = await self.nasa_daily_image()
        embed, video = create_nasa_embed(response)
        await inter.edit_original_response(embed=embed)
        if video:
            await inter.followup.send(video)

    @tasks.loop(time=time(7, 0, tzinfo=utils.get_local_zone()))
    async def send_nasa_image(self):
        response = await self.nasa_daily_image()
        embed, video = create_nasa_embed(response)
        for channel in self.nasa_channels:
            await channel.send(embed=embed)
            if video:
                await channel.send(video)

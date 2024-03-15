"""
Cog for sending name days and birthdays.
"""

import asyncio
from datetime import date, time

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

import utils.utils as utils
from cogs.base import Base
from custom import room_check
from custom.cooldowns import default_cooldown

from .messages import NameDayMess


class NameDay(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.tasks = [self.send_names.start()]
        self._owner_id = bot.owner_id
        self.check = room_check.RoomCheck(bot)

    async def _name_day_cz(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                url = f"http://svatky.adresa.info/json?date={date.today().strftime('%d%m')}"
                async with session.get(url) as resp:
                    res = await resp.json()
                names = []
                for i in res:
                    names.append(i["name"])
                return NameDayMess.name_day_cz(name=", ".join(names))
            except (asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError):
                return "Website unreachable"

    async def _name_day_sk(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                url = f"http://svatky.adresa.info/json?lang=sk&date={date.today().strftime('%d%m')}"
                async with session.get(url) as resp:
                    res = await resp.json()
                names = []
                for i in res:
                    names.append(i["name"])
                return NameDayMess.name_day_sk(name=", ".join(names))
            except (asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientConnectorError):
                return "Website unreachable"

    @default_cooldown()
    @app_commands.command(name="svatek", description=NameDayMess.name_day_cz_brief)
    async def name_day_cz(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=self.check.botroom_check(inter))
        name_day_cz = await self._name_day_cz()
        await inter.edit_original_response(name_day_cz)

    @default_cooldown()
    @app_commands.command(name="meniny", description=NameDayMess.name_day_sk_brief)
    async def name_day_sk(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=self.check.botroom_check(inter))
        name_day_sk = await self._name_day_sk()
        await inter.edit_original_response(name_day_sk)

    @tasks.loop(time=time(7, 0, tzinfo=utils.get_local_zone()))
    async def send_names(self):
        name_day_cz = await self._name_day_cz()
        name_day_sk = await self._name_day_sk()
        mentions = discord.AllowedMentions.none()
        await self.name_day_channel.send(f"{name_day_cz}\n{name_day_sk}", allowed_mentions=mentions)

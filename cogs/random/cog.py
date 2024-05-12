from __future__ import annotations

import random
import shlex
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from cogs.base import Base
from custom.cooldowns import default_cooldown

if TYPE_CHECKING:
    from morpheus import Morpheus


class Random(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot

    @default_cooldown()
    @app_commands.command(name="flip", description="flip a coin")
    async def flip(self, inter: discord.Interaction):
        await inter.response.send_message(random.randint(0, 1))

    @default_cooldown()
    @app_commands.command(name="roll", description="Roll a dice for range")
    async def roll(self, inter: discord.Interaction, x: int, y: int = 0):
        if x > y:
            x, y = y, x
        await inter.response.send_message(str(random.randint(x, y)))

    @default_cooldown()
    @app_commands.command(name="pick", description="Pick a random thing")
    async def pick(self, inter: discord.Interaction, args: str):
        args = shlex.split(args)

        option = discord.utils.escape_mentions(random.choice(args))
        await inter.response.send_message(f"{option[:1900]} {inter.author.mention}")

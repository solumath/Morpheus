from __future__ import annotations

from typing import TYPE_CHECKING

import discord
import git
from discord import app_commands
from discord.ext import commands

import utils.utils as utils
from cogs.base import Base
from custom.cooldowns import default_cooldown
from custom.permission_check import is_bot_admin
from utils import embed_utils

from . import features
from .buttons import SystemView
from .messages import SystemMess

if TYPE_CHECKING:
    from morpheus import Morpheus


class Git:
    def __init__(self):
        self.repo = git.Repo(search_parent_directories=True)
        self.cmd = self.repo.git

    async def pull(self):
        return self.cmd.pull()

    def short_hash(self):
        return self.repo.head.object.hexsha[:7]


class System(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot
        self.git = Git()

        self.unloadable_cogs = ["system"]

    git_group = app_commands.Group(name="git", description=SystemMess.git_brief)

    @app_commands.check(is_bot_admin)
    @git_group.command(name="pull", description=SystemMess.git_pull_brief)
    async def pull(self, inter: discord.Interaction):
        await inter.response.send_message("`Pulling`")
        message = await inter.original_response()

        pull_result = await self.git.pull()
        pull_parts = utils.cut_string(pull_result, 1900)

        await message.edit(content=f"```{pull_parts[0]}```")

        for part in pull_parts[1:]:
            await inter.followup.send(f"```{part}```")

    @app_commands.check(is_bot_admin)
    @app_commands.command(name="shutdown", description=SystemMess.shutdown_brief)
    async def shutdown(self, inter: discord.Interaction):
        await inter.response.send_message("`Shutting down...`")
        exit(1)

    @app_commands.check(is_bot_admin)
    @app_commands.command(name="cogs", description=SystemMess.cogs_brief)
    async def cogs(self, inter: discord.Interaction):
        """
        Creates embed with button and select(s) to load/unload/reload cogs.

        Max number of cogs can be 100 (4x25).
        """
        await inter.response.defer()
        cog_chunks = await features.split_cogs()
        view = SystemView(self.bot, cog_chunks)
        embed = features.create_embed(self.bot)
        message = await inter.followup.send(embed=embed, view=view)

        # pass message object to classes
        view.message = message
        for i in range(len(cog_chunks)):
            view.selects[i].message = message

    @default_cooldown()
    @app_commands.command(name="morpheus", description=SystemMess.morpheus_brief)
    async def morpheus(self, inter: discord.Interaction):
        await inter.response.defer()
        embed = embed_utils.info_embed(self.bot)
        await inter.edit_original_response(embed=embed)

    @cogs.error
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error.__cause__, commands.errors.ExtensionNotLoaded):
            await ctx.send(SystemMess.not_loaded.format(error.__cause__.name))
            return True

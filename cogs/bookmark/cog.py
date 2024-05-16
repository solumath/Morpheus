from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from cogs.base import Base

from .buttons import BookmarkModal, BookmarkView
from .features import BookmarkContext, BookmarkFeatures

if TYPE_CHECKING:
    from morpheus import Morpheus


class Bookmark(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(name="Bookmark", callback=self.bookmark)
        self.bot.tree.add_command(self.ctx_menu)

    @commands.Cog.listener("on_ready")
    async def init_views(self):
        """Add permanent views to the bot"""
        self.bot.add_view(BookmarkView())

    @app_commands.guild_only()
    async def bookmark(self, inter: discord.Interaction, message: discord.Message):
        """Send modal with input for bookmark name and then send to user"""
        await inter.response.send_modal(BookmarkModal(message))

    @commands.Cog.listener("on_raw_reaction_add")
    async def bookmark_reaction(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name != "🔖":
            return

        ctx = BookmarkContext(self.bot, payload)
        await ctx.get_context()

        embed, images, files_attached = await BookmarkFeatures.create_bookmark_embed(self, ctx)
        if images:
            for image in images:
                embed.append(await BookmarkFeatures.create_image_embed(self, ctx, image))
        # when sending sticker there can be overflow of files
        if len(files_attached) <= 10:
            await payload.member.send(embeds=embed, view=BookmarkView(ctx.message.jump_url), files=files_attached)
        else:
            await payload.member.send(embeds=embed, view=BookmarkView(ctx.message.jump_url), files=files_attached[:10])
            await payload.member.send(files=files_attached[10:])

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

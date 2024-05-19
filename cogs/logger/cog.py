from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from cogs.base import Base

from .levels import LoggerLeveles
from .top_logger import top_logger

if TYPE_CHECKING:
    from morpheus import Morpheus


class Logger(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot

    @staticmethod
    def log_prefix(channel: discord.abc.GuildChannel, message: str, author: discord.User) -> str:
        author = f"{author.display_name}({author.id})" if author else "Unknown Author"
        return f"Channel: {channel}, Message: {message}, Author: {author}"

    @commands.Cog.listener("on_message")
    async def on_message_log(self, message: discord.Message):
        if message.author.bot:
            return

        if message.guild is None:
            return

        if message.embeds:
            for embed in message.embeds:
                content = embed.to_dict()
        else:
            content = message.content

        attachments = []
        if "Traceback" not in message.content:
            if message.attachments:
                for x in message.attachments:
                    attachments.append(x.url)

        prefix = self.log_prefix(message.channel, message.jump_url, message.author)
        logger = top_logger.get_guild_logger(message.guild.id)
        logger.message_logger.log(LoggerLeveles.Message, f"{prefix}, Content: {content}, Attachments: {attachments}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if self.bot.user.id == payload.user_id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)

        prefix = self.log_prefix(channel, message.jump_url, author)
        logger = top_logger.get_guild_logger(payload.guild_id)
        logger.reaction_logger.log(LoggerLeveles.Reaction, f"{prefix}, Remove: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self.bot.user.id == payload.user_id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        author = guild.get_member(payload.user_id)

        prefix = self.log_prefix(channel, message.jump_url, author)
        logger = top_logger.get_guild_logger(payload.guild_id)
        logger.reaction_logger.log(LoggerLeveles.Reaction, f"{prefix}, Add: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        if payload.cached_message:
            message = payload.cached_message
            channel = message.channel
        else:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

        if message.author.bot:
            return

        prefix = self.log_prefix(channel, message.jump_url, message.author)
        logger = top_logger.get_guild_logger(payload.guild_id)
        logger.message_logger.log(LoggerLeveles.Edit, f"{prefix}, Content: {message.content}")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):
        if payload.cached_message:
            message = payload.cached_message
            author = message.author
        else:
            author = None
            message = None

        if author and author.id == self.bot.user.id:
            return

        if message:
            if message.embeds:
                for embed in message.embeds:
                    content = embed.to_dict()
            else:
                content = message.content

            attachments = []
            if "Traceback" not in message.content:
                if message.attachments:
                    for x in message.attachments:
                        attachments.append(x.url)
        else:
            content = ""
            attachments = ""

        channel = self.bot.get_channel(payload.channel_id)

        prefix = self.log_prefix(channel, payload.message_id, author)
        logger = top_logger.get_guild_logger(payload.guild_id)
        logger.message_logger.log(LoggerLeveles.Delete, f"{prefix}, Content: {content}, Attachments: {attachments}")

    @commands.Cog.listener()
    async def on_command(self, inter: discord.Interaction):
        prefix = self.log_prefix(inter.channel, inter.message.jump_url, inter.user)
        logger = top_logger.get_guild_logger(inter.guild.id)
        logger.command_logger.log(
            LoggerLeveles.Command,
            f"{prefix}, Command: {inter.prefix}{inter.command.name}, Passed: {inter.kwargs}",
        )

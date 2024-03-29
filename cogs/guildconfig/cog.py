import random

import discord
from discord import app_commands
from discord.ext import commands

from cogs.base import Base
from custom.cooldowns import default_cooldown
from database.guild import GuildDB, GuildPhraseDB

from .messages import GuildConfigMess


@app_commands.guild_only()
@default_cooldown()
class ReplyGroup(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GuildConfig(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.phrases = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.phrases[guild.id] = GuildDB.get_guild(guild.id).phrases_dict

    reply_group = ReplyGroup(name="reply", description="Autoreply commands")

    @commands.has_permissions(administrator=True)
    @app_commands.guild_only()
    @default_cooldown()
    @app_commands.command(name="edit_config", description=GuildConfigMess.edit_config_brief)
    async def edit_config(self, inter: discord.Interaction, info_channel: discord.TextChannel):
        """for now only info channel in future all attributes guild config can have"""
        guild_db = GuildDB.get_guild(inter.guild.id)
        guild_db.set_info_channel(info_channel.id)
        await inter.response.send_message(GuildConfigMess.info_channel_set(info_channel=info_channel.mention))

    @commands.Cog.listener("on_message")
    async def reply(self, message: discord.Message):
        """sends messages to users depending on the content"""
        if message.guild is None:
            return

        if message.author.bot:
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif f"<@!{self.bot.user.id}>" in message.content or f"<@{self.bot.user.id}>" in message.content:
            await message.channel.send(random.choice(GuildConfigMess.Morpheus))
        else:
            phrases = self.phrases.get(message.guild.id)
            if not phrases:
                return
            for key, value in phrases.items():
                if key.lower() == message.content.lower():
                    await message.channel.send(value)

    @reply_group.command(name="add", description=GuildConfigMess.add_reply_brief)
    async def add_reply(self, inter: discord.Interaction, key: str, reply: str):
        phrase = GuildPhraseDB.add_phrase(inter.guild.id, key, reply)
        if not phrase:
            await inter.response.send_message(GuildConfigMess.reply_exists(key=key))
            return

        self.phrases[inter.guild.id] = GuildDB.get_guild(inter.guild.id).phrases_dict
        await inter.response.send_message(GuildConfigMess.reply_added(key=key))

    @reply_group.command(name="remove", description=GuildConfigMess.rem_reply_brief)
    async def remove_reply(self, inter: discord.Interaction, key: str):
        phrase = GuildPhraseDB.remove_phrase(inter.guild.id, key)
        if not phrase:
            await inter.response.send_message(GuildConfigMess.reply_not_found(key=key))
            return

        self.phrases[inter.guild.id] = GuildDB.get_guild(inter.guild.id).phrases_dict
        await inter.response.send_message(GuildConfigMess.reply_removed(key=key))

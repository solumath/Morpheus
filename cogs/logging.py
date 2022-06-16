from disnake.ext import commands
from logging.handlers import TimedRotatingFileHandler

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler(filename=f"servers/logs/L", when="midnight", interval=1, encoding='utf-8', backupCount=31)
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
handler.suffix = "%d.%m.%Y.log"
logger.addHandler(handler)

logging.addLevelName(21, "MSG")
logging.addLevelName(22, "REACT")
logging.addLevelName(23, "EDIT")
logging.addLevelName(24, "DEL")
logging.addLevelName(25, "COMM")

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #-------------------------Logs----------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        logger.log(22, f"Guild: {message.guild} || Channel: {channel} || Message: {message.id} ||"
                       f" Author: {member} || EmojiRem: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        logger.log(22, f"Guild: {message.guild} || Channel: {channel} || Message: {message.id} ||" 
                       f" Author: {payload.member} || EmojiAdd: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        logger.log(23, f"Guild: {message.guild} || Channel: {channel} || Message: {message.id} ||" 
                       f" Author: {message.author}: {message.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        logger.log(24, f"Guild: {ctx.guild} || Channel: {ctx.channel} || Message: {ctx.id} ||" 
                       f" Author: {ctx.author}: {ctx.content}")

    @commands.Cog.listener()
    async def on_slash_command(self, inter):
        guild = self.bot.get_guild(inter.guild_id)
        logger.log(25, f"Guild: {guild} || Channel: {inter.channel} || Message: {inter.id} ||"
                       f" Author: {inter.author} || Command: {inter.data.name} || Passed: {inter.filled_options}")


def setup(bot):
    bot.add_cog(Logging(bot))

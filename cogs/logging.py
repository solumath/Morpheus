import disnake
from disnake.ext import commands
from logging.handlers import TimedRotatingFileHandler

import re
import json
import logging
import random
from config.messages import Messages

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

    @commands.slash_command(name="addreply", description="Add autoreply")
    async def addreply(self, inter: disnake.ApplicationCommandInteraction, key, reply):
        with open(f"servers/{inter.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            if key.lower() in dict.keys():
                await inter.response.send_message(f"hláška {key} již existuje")
            else:
                add = {f"{key.lower()}":reply}
                dict.update(add)
                with open(f"servers/{inter.guild.name}/replies.json",'w', encoding='utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                await inter.response.send_message(f"reply {key} byla přidána")

    @commands.slash_command(name="remreply", description="Remove autoreply")
    async def remreply(self, inter: disnake.ApplicationCommandInteraction, key):
        with open(f"servers/{inter.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            if key.lower() in dict.keys():
                dict.pop(key.lower())
                with open(f"servers/{inter.guild.name}/replies.json", 'w', encoding='utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                await inter.response.send_message(f"hláška {key} byla odstraněna")
            else:
                await inter.response.send_message(f"takovou hlášku jsem nenašel")

    @commands.Cog.listener("on_message")
    async def reply(self, message):
        """sends messages to users depending on the content"""

        if message.embeds:
            for embed in message.embeds:
                content = embed.to_dict()
        else:
            content = message.content

        if not "Traceback" in message.content:
            image = []
            if message.attachments:
                for x in message.attachments:
                    image.append(x.url)

            logger.log(21, f"Guild: {message.guild} || Channel: {message.channel} || Message: {message.id} ||"
                           f" Author: {message.author}: {content} {image}")

        if message.guild is None:
            return

        with open(f"servers/{message.guild.name}/replies.json", 'r') as f:
            replies = json.load(f)

        if message.author.bot:
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif f"<@!{self.bot.user.id}>" in message.content or f"<@{self.bot.user.id}>" in message.content:
            await message.channel.send(random.choice(Messages.Morpheus))
        else: 
            for key, value in replies.items():
                if re.search(fr"^\b{key.lower()}\b", message.content.lower()):
                    await message.channel.send(value)

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

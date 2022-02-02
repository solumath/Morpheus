import disnake
from disnake.ext import commands
from logging.handlers import TimedRotatingFileHandler

import os
import json
import logging
import traceback
import random

import env
from config import messages

messages = messages.Messages

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
    async def addreply(self, ctx, key, reply):
        with open(f"servers/{ctx.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            if key in dict.keys():
                await ctx.send(f"hláška {key} již existuje")
            else:
                add = {f"{key}":reply}
                dict.update(add)
                with open(f"servers/{ctx.guild.name}/replies.json",'w', encoding='utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                await ctx.send(f"reply {key} byla přidána")

    @commands.slash_command(name="remreply", description="Remove autoreply")
    async def remreply(self, ctx, key):
        with open(f"servers/{ctx.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            if key in dict.keys():
                dict.pop(key)
                with open(f"servers/{ctx.guild.name}/replies.json", 'w', encoding='utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                await ctx.send(f"hláška {key} byla odstraněna")
            else:
                await ctx.send(f"takovou hlášku jsem nenašel")

    #uh oh reply
    @commands.Cog.listener("on_message")
    async def reply(self, message):
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
            await message.channel.send(random.choice(messages.Morpheus))
        elif message.content in replies.keys():
            await message.channel.send(replies[message.content])

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
    async def on_slash_command(self, ctx):
        guild = self.bot.get_guild(ctx.guild_id)
        print(dir(ctx.data))
        args = ""
        if ctx.filled_options is not None:
            args = list(ctx.filled_options)
        logger.log(25, f"Guild: {guild} || Channel: {ctx.channel} || Message: {ctx.application_id} ||"
                       f" Author: {ctx.author} || Command: {ctx.data.name} || Passed: {ctx.filled_options}")

    #-------------------------Errors----------------------------
    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not posses enough strenght to beat me!")

        #send traceback to server
        else:
            await ctx.defer()
            channel = self.bot.get_channel(env.development)

            lines = traceback.format_exception(type(error), error, error.__traceback__)
            ex = ''.join(lines)
            
            logger.exception(ex)
            
            message = await ctx.send(f"```Errors happen Mr. Anderson```")
            
            embed = disnake.Embed(title=f"Ignoring exception on {ctx.command}", colour=0xFF0000)
            embed.add_field(name="Zpráva", value=ctx.kwargs, inline=True)
            embed.add_field(name="Autor", value=ctx.author, inline=True)
            embed.add_field(name="Link", value=message.jump_url, inline=False)
            embed.add_field(name="Traceback", value=f"```{ex}```", inline=False)

            print(ex)
            await channel.send(embed=embed)

            raise error

def setup(bot):
    bot.add_cog(Logging(bot))
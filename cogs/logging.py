import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import os
import json
import datetime
import git
import logging
import traceback

today = datetime.date.today()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f"servers/logs/{today}.log",encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger.addHandler(handler)
logging.addLevelName(21, "MSG")
logging.addLevelName(22, "REACT")
logging.addLevelName(23, "EDIT")
logging.addLevelName(24, "DEL")
logging.addLevelName(25, "COMM")

class Autoreplies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as', self.bot.user)
        print('ID:', self.bot.user.id)

        #set status for bot
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        await self.bot.change_presence(activity=discord.Game(f"/userinfo | On commit {sha[:7]}"))

    @cog_ext.cog_slash(name="addreply", description="Add autoreply")
    async def addreply(self, ctx, key, reply):
        with open(f"servers/{ctx.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            add = json.load(f)
            f.seek(0, 0)
            f.truncate(0)
            if key in add.keys():
                await ctx.send(f"hláška {key} již existuje")
            else:
                add[key] = reply
                json.dump(add, f, ensure_ascii=False, indent=4)
                await ctx.send(f"reply {key} byla přidána")

    @cog_ext.cog_slash(name="remreply", description="Remove autoreply")
    async def remreply(self, ctx, key):
        with open(f"servers/{ctx.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            rem = json.load(f)
            f.seek(0, 0)
            f.truncate(0)
            if key in rem.keys():
                del rem[key]
                json.dump(rem, f, ensure_ascii=False, indent=4)
                await ctx.send(f"hláška {key} byla odstraněna")
            else:
                await ctx.send(f"takovou hlášku jsem nenašel")

    #uh oh reply
    @commands.Cog.listener()
    async def on_message(self, message):
        if not "Traceback" in message.content:
            image = ""
            if message.attachments:
                image = message.attachments[0].url
            logger.log(21, f"Guild: {message.guild} || Channel: {message.channel} || Message: {message.id} ||"
                           f" Author: {message.author}: {message.content} {image}")

        if message.guild is None:
            return

        with open(f"servers/{message.guild.name}/replies.json", 'r') as f:
            replies = json.load(f)

        if message.author.bot:
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif f"<@!{self.bot.user.id}>" in message.content or f"<@{self.bot.user.id}>" in message.content:
            await message.channel.send("Remember...All I'm Offering Is The Truth. Nothing More.")
        elif message.content in replies.keys():
            await message.channel.send(replies[message.content])

    #-------------------------Logs----------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await self.bot.fetch_user(payload.user_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        logger.log(22, f"Guild: {guild} || Channel: {channel} || Message: {payload.message_id} ||"
                       f" Author: {member} || EmojiRem: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = await self.bot.fetch_user(payload.user_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        logger.log(22, f"Guild: {guild} || Channel: {channel} || Message: {payload.message_id} ||" 
                       f" Author: {member} || EmojiAdd: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        channel = await self.bot.fetch_channel(payload.channel_id)
        logger.log(23, f"Guild: {guild} || Channel: {channel} || Message: {payload.message_id} ||" 
                       f" Author: {payload.data['author']['username']}#{payload.data['author']['discriminator']}:"
                       f" {payload.data['content']}")
    
    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        logger.log(24, f"Guild: {ctx.guild} || Channel: {ctx.channel} || Message: {ctx.id} ||" 
                       f" Author: {ctx.author}: {ctx.content}")
    
    @commands.Cog.listener()
    async def on_slash_command(self, ctx):
        args = ""
        if ctx.kwargs is not None:
            args = list(ctx.kwargs.values())
        logger.log(25, f"Guild: {ctx.guild} || Channel: {ctx.channel} || Message: {ctx.interaction_id} ||"
                       f" Author: {ctx.author} || Command: {ctx.command} || Passed: {args}")

    #-------------------------Errors----------------------------
    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("I do not posses that command")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You cannot beat me!")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Your argument is invalid")

        #send traceback to server
        else:
            channel = self.bot.get_channel(768796879042773022)
            etype = type(error)
            trace = error.__traceback__
            lines = traceback.format_exception(etype, error, trace)
            traceback_text = ''.join(lines)

            logger.exception(traceback_text)
            await ctx.send(f"```{traceback_text}```")
            await channel.send(f"```{traceback_text}```")
            raise error
    
def setup(bot):
    bot.add_cog(Autoreplies(bot))
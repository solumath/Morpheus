import discord
from discord.ext import commands
from discord_slash import cog_ext
import os
import json
import datetime
import git
import logging

today = datetime.date.today()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename=f"servers/logs/{today}.log",encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
logger.addHandler(handler)
logging.addLevelName(21, "MSG")
logging.addLevelName(22, "REACTION")
logging.addLevelName(23, "EDIT")

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
        if message.guild is None:
            return

        with open(f"servers/{message.guild.name}/replies.json", 'r') as f:
            replies = json.load(f)

        if message.author.bot:
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif (f'<@!{self.bot.user.id}>') in message.content:
            await message.channel.send("Remember...All I'm Offering Is The Truth. Nothing More.")
        elif message.content in replies.keys():
            await message.channel.send(replies[message.content])

        #------------------Logger--------------------------------------
        logger.log(21, "%s || %s || %s: %s", message.guild, message.channel, message.author.name, message.content)

        # with open(f"servers/{message.guild.name}/logs/{today}","a+") as f:
        #     f.write(f"{message.guild.name}; {today}, {current_time}: {message.author.name}: {message.content}\n")
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        logger.log(22, "Guild %s || Channel %s || Message %s || Member %s un-reacted || Emoji %s",
                    payload.guild_id, payload.channel_id,payload.message_id, payload.member, payload.emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        logger.log(22, "Guild %s || Channel %s || Message %s || Member %s reacted || Emoji %s",
                    payload.guild_id, payload.channel_id,payload.message_id, payload.member, payload.emoji)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        logger.log(23, "Guild %s || Channel %s || Message %s || Member %s",
                    payload.guild_id, payload.channel_id,payload.message_id, payload.data['member']['nick'])

def setup(bot):
    bot.add_cog(Autoreplies(bot))

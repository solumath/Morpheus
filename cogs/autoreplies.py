import discord
from discord.ext import commands
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
        await self.bot.change_presence(activity=discord.Game(f"?help | On commit {sha[:7]}"))

    @commands.command()
    async def addreply(self, ctx, key, reply):
        """add autoreply to db"""
        with open(f"servers/{ctx.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            add = json.load(f)
            f.seek(0, 0)
            f.truncate(0)
            if key in add.keys():
                await ctx.send(f"hláška {key} již existuje")
            else:
                add[key] = reply
                json.dump(add, f, ensure_ascii=False, indent=4)
                await ctx.send(f"hláška {key} byla přidána")

    @commands.command()
    async def remreply(self, ctx, key):
        """remove autoreply from db"""
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
    @commands.Cog.listener()                                          #actually @bot.event
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
            await message.channel.send("Co mě pinguješ?! Chceš jednu dostat <:Reee:747845163279319180>?! Použij ?help ")
        elif message.content in replies.keys():
            await message.channel.send(replies[message.content])

        #------------------Logger--------------------------------------
        logger.log(21, "%s: %s", message.author.name, message.content)

        # with open(f"servers/{message.guild.name}/logs/{today}","a+") as f:
        #     f.write(f"{message.guild.name}; {today}, {current_time}: {message.author.name}: {message.content}\n")
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        logger.info("in %s, %s un-reacted with %s on message: %s",
                    payload.guild.name, payload.member.name, payload.emoji.name, payload.message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        logger.info("in %s, %s reacted with %s on message: %s",
                    payload.guild.name, payload.member.name, payload.emoji.name, payload.message_id)

def setup(bot):
    bot.add_cog(Autoreplies(bot))

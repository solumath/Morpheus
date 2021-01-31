import discord
from datetime import date
from datetime import datetime
from discord.ext import commands
import os
import json

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as', self.bot.user)
        print('ID:', self.bot.user.id)

    #uh oh reply
    @commands.Cog.listener()                                          #actually @bot.event
    async def on_message(self, message):
        with open("src/replies.json", 'r') as fp:
            replies = json.load(fp)

        if message.author.bot:
            if message.author.id == self.bot.user.id and \
                message.content.startswith("<:") and \
                message.content.endswith(">"):
                 await message.channel.send(message.content)
            return

        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif message.content in replies.keys():
            await message.channel.send(replies[message.content])

        #------------------Logger--------------------------------------
        now = datetime.now()
        today = date.today()
        today = today.strftime("%d.%m.%Y")
        current_time = now.strftime("%H:%M:%S")

         #----------------------Create dir-----------------------------
        if not (os.path.isdir(f"logs/{message.guild.name}")):
                os.mkdir(f"logs/{message.guild.name}")
        with open(f"logs/{message.guild.name}/{today}","a+") as f:
            f.write(f"{message.guild.name}; {today}, {current_time}: {message.author.name}: {message.content}\n")

    @commands.command()
    async def kredity(self, ctx):
        """prints out credits for BIT"""
        await ctx.send("""
        ```cs
if ("pokazil jsem volitelný" or "Pokazil jsem aspoň 2 povinné")
    return 65
if ("Pokazil jsem 1 povinný" or "Mám průměr nad 2.0")
    return 70
if ("Mám průměr pod 1.5")
    return 80
if ("Mám průměr pod 2.0")
    return 75```""")

def setup(bot):
    bot.add_cog(Memes(bot))
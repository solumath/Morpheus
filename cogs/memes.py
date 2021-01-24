import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='?')

class memes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ready!')
        print('Logged in as ', self.bot.user)
        print('ID:', self.bot.user.id)
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='?')

class memes(commands.Cog):

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
        if message.author.bot:
            if message.author.id == self.bot.user.id and \
                message.content.startswith("<:") and \
                message.content.endswith(">"):
                 await message.channel.send(message.content)
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")

def setup(bot):
    bot.add_cog(memes(bot))
    #uh oh reply
    @commands.Cog.listener()                                          #actually @bot.event
    async def on_message(self, message):
        if message.author.bot:
            if message.author.id == self.bot.user.id and \
                message.content.startswith("<:") and \
                message.content.endswith(">"):
                 await message.channel.send(message.content)
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif "cs" in message.content:
            await message.channel.send("henlo <:peepolove:747845162071490742>")

def setup(bot):
    bot.add_cog(memes(bot))
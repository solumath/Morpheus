import disnake
from config.app_config import config
from disnake.ext import commands
from disnake.channel import TextChannel


mention_count = {}

async def iterate_messages(channel):
    history = await channel.history(limit=None).flatten()
    for message in history:
        if message.author.bot:
            continue
        for mention in message.mentions:
            if mention not in mention_count:
                mention_count[mention] = 0
            mention_count[mention] += 1

class Gays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="leadgay", description="Gay leaderboard")
    async def gays(self, inter: disnake.ApplicationCommandInteraction):
        global mention_count
        await inter.response.defer()
        for guild in self.bot.guilds:
            if(guild.id != config.guild_id):
                continue
            for channel in guild.channels:
                if(channel.id != config.bot_gay_channel):
                    continue
                if isinstance(channel, TextChannel):
                    await iterate_messages(channel)
        mention_count = dict(sorted(mention_count.items(), key=lambda item: item[1], reverse=True)[:10])
        output = '# Naši nejlepší gejové:\n```'
        for mention, count in mention_count.items():
            output += f'{mention.name}: {count}\n'
        output += '```'
        await inter.edit_original_response(output)


def setup(bot):
    bot.add_cog(Gays(bot))

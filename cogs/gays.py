import disnake
from config.app_config import config
from disnake.ext import commands
from disnake.channel import TextChannel


mention_count = {}
mention_author_count = {}

def first_in_day(message, prev_message_day):
    if prev_message_day is None:
        return True
    # WARN: Can be wrong if the next message is month after at the same day
    return message.created_at.day != prev_message_day

async def iterate_messages(channel):
    history = await channel.history(limit=None).flatten()
    prev_message_day = None
    for message in history:
        if message.author.bot:
            continue

        if not first_in_day(message, prev_message_day):
            continue

        if not len(message.mentions):
            continue

        for mention in message.mentions:
            if mention not in mention_count:
                mention_count[mention] = 0
            mention_count[mention] += 1

        if message.author not in mention_author_count:
            mention_author_count[message.author] = 0
        mention_author_count[message.author] += 1
        prev_message_day = message.created_at.day

class Gays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="leadgay", description="Gay leaderboard")
    async def gays(self, inter: disnake.ApplicationCommandInteraction, count: int = 10):
        global mention_author_count, mention_count
        mention_author_count = {}
        mention_count = {}
        await inter.response.defer()
        guild = self.bot.get_guild(config.guild_id)
        channel = guild.get_channel(config.bot_gay_channel)
        if isinstance(channel, TextChannel):
            await iterate_messages(channel)
       
        mention_count_sorted = dict(sorted(mention_count.items(), key=lambda item: item[1], reverse=True)[:count])
        output = '# Naši nejlepší gejové:\n```'
        for mention, tag_count in mention_count_sorted.items():
            output += f'{mention.name}: {tag_count}\n'
        output += '```\n'

        mention_author_count_sorted = dict(sorted(mention_author_count.items(), key=lambda item: item[1], reverse=True)[:count])
        output += '# Naši nejlepší tagři:\n```'
        for mention, tag_count in mention_author_count_sorted.items():
            output += f'{mention.name}: {tag_count}\n'
        output += '```'

        await inter.edit_original_response(output)


def setup(bot):
    bot.add_cog(Gays(bot))

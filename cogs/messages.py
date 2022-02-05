import disnake
from disnake.ext import commands

class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="Messages", description="Count all messages from everyone")
    async def messages(self, ctx):
        members = []
        messages = []
        text_channels = []
        for channel in ctx.guild.text_channels:
            text_channels.append(channel)
        for member in ctx.guild.members:
            members.append(member.name)
            messages.append(0)
        for chan in text_channels:
            for index, member in enumerate(members):
                async for message in chan.history(limit=None):
                    if message.author.name == member:
                        messages[index] += 1
        
        zip_iterator = zip(members, messages)
        messages_of_members = dict(zip_iterator)
        
        await ctx.send(messages_of_members)

def setup(bot):
    bot.add_cog(Messages(bot))

from disnake.ext import commands


class Logger(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener("on_message")
    async def on_message_log(self, message):
        if message.embeds:
            for embed in message.embeds:
                content = embed.to_dict()
        else:
            content = message.content

        image = []
        if "Traceback" not in message.content:
            if message.attachments:
                for x in message.attachments:
                    image.append(x.url)

        self.logger.log(21, f"Guild: {message.guild} || Channel: {message.channel} || "
                            f"Message: {message.id} || Author: {message.author}: {content} {image}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        self.logger.log(22, f"Guild: {message.guild} || Channel: {channel} || Message: {message.id} ||"
                            f" Author: {member} || EmojiRem: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        self.logger.log(22, f"Guild: {message.guild} || Channel: {channel} || Message: {message.id} ||"
                            f" Author: {payload.member} || EmojiAdd: {payload.emoji}")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        self.logger.log(23, f"Guild: {message.guild} || Channel: {channel} || Message: {message.id} ||"
                            f" Author: {message.author}: {message.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        self.logger.log(24, f"Guild: {ctx.guild} || Channel: {ctx.channel} || Message: {ctx.id} ||"
                            f" Author: {ctx.author}: {ctx.content}")

    @commands.Cog.listener()
    async def on_slash_command(self, inter):
        guild = self.bot.get_guild(inter.guild_id)
        self.logger.log(25, f"Guild: {guild} || Channel: {inter.channel} || "
                            f"Message: {inter.id} || Author: {inter.author} || "
                            f"Command: {inter.data.name} || Passed: {inter.filled_options}")

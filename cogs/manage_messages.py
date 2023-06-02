import json
import os
import random
import time

import disnake
import pytz
import requests
from disnake.ext import commands

from config.app_config import config
from config.messages import Messages


class ManageMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @commands.slash_command(name="purge", description="Delete number of messages")
    async def purge(ctx, number_of_messages: int):
        await ctx.channel.purge(limit=number_of_messages)
        await ctx.send("Poof", delete_after=5)

    @commands.slash_command(name="addreply", description="Add autoreply")
    async def addreply(self, inter: disnake.ApplicationCommandInteraction, key, reply):
        with open(f"servers/{inter.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            if key.lower() in dict.keys():
                await inter.response.send_message(f"hláška {key} již existuje")
            else:
                add = {f"{key.lower()}": reply}
                dict.update(add)
                with open(f"servers/{inter.guild.name}/replies.json", 'w', encoding='utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                await inter.response.send_message(f"reply {key} byla přidána")

    @commands.slash_command(name="remreply", description="Remove autoreply")
    async def remreply(self, inter: disnake.ApplicationCommandInteraction, key):
        with open(f"servers/{inter.guild.name}/replies.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            if key.lower() in dict.keys():
                dict.pop(key.lower())
                with open(f"servers/{inter.guild.name}/replies.json", 'w', encoding='utf-8') as f:
                    json.dump(dict, f, ensure_ascii=False, indent=4)
                await inter.response.send_message(f"hláška {key} byla odstraněna")
            else:
                await inter.response.send_message("takovou hlášku jsem nenašel")

    @commands.Cog.listener("on_message")
    async def reply(self, message):
        """sends messages to users depending on the content"""

        if message.guild is None:
            return

        with open(f"servers/{message.guild.name}/replies.json", 'r') as f:
            replies = json.load(f)

        if message.author.bot:
            return
        elif "uh oh" in message.content:
            await message.channel.send("uh oh")
        elif f"<@!{self.bot.user.id}>" in message.content or f"<@{self.bot.user.id}>" in message.content:
            await message.channel.send(random.choice(Messages.Morpheus))
        else:
            for key, value in replies.items():
                if key.lower() == message.content.lower():
                    await message.channel.send(value)

    @commands.has_permissions(administrator=True)
    @commands.command(name="count", description="Count all messages from everyone")
    async def message_count(self, ctx):
        member_ids = [member.id for member in ctx.guild.members]
        messages_count = {}
        headers = {'authorization': config.key}
        for ids in member_ids:
            r = requests.get(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/messages/search?author_id={ids}&include_nsfw=true', headers=headers)  # noqa: E501
            data = json.loads(r.text)
            username = ctx.guild.get_member(ids)

            messages_count.update({ids: data['total_results']})
            await ctx.send(f"**Jméno**= {username}; **ID**= {ids}; **počet zpráv**= {data['total_results']}")
            # prevent rate limit
            time.sleep(2)

        with open(f"servers/{ctx.guild.name}/messages.json", 'w', encoding='utf-8') as f:
            json.dump(messages_count, f, ensure_ascii=False, indent=4)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="history", description=Messages.channel_history_brief)
    async def channel_history(
            self,
            inter,
            channel: disnake.TextChannel,
            old_to_new: bool = commands.Param(default=True, description="Sort messages chronologically"),
            limit: int = commands.Param(default=None, description="Number of messages to retrieve")
            ):
        await inter.send(Messages.channel_history_retrieving_messages.format(channel.mention))
        messages = await channel.history(limit=limit, oldest_first=old_to_new).flatten()

        users = {}
        with open(f"{channel}_users.txt", "w") as file:
            for message in messages:
                users[message.author.id] = message.author.name

            for user_id, user_name in users.items():
                file.write(f"{user_id} | {user_name}\n")

        timezone = pytz.timezone('Europe/Prague')
        with open(f"{channel}_history.txt", "w") as file:
            for message in messages:
                utc_now = message.created_at
                time = utc_now.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")
                content = message.content.replace("\n", " ")
                author = str(message.author.id).ljust(len(str(message.author.id)), " ")
                file.write(f"{time} | {author} | {content}\n")

        await inter.author.send(file=disnake.File(f"{channel}_history.txt"))
        await inter.author.send(file=disnake.File(f"{channel}_users.txt"))
        await inter.edit_original_message(Messages.channel_history_success.format(channel))

        if os.path.exists(f"{channel}_history.txt"):
            os.remove(f"{channel}_history.txt")
        if os.path.exists(f"{channel}_users.txt"):
            os.remove(f"{channel}_users.txt")


def setup(bot):
    bot.add_cog(ManageMessages(bot))

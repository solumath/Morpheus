from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from cogs.base import Base

from .messages import AdminMess

if TYPE_CHECKING:
    from morpheus import Morpheus


class Admin(Base, commands.Cog):
    def __init__(self, bot: Morpheus):
        super().__init__()
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @app_commands.command(name="purge", description=AdminMess.purge_brief)
    @app_commands.describe(last_message_url=AdminMess.last_message_param)
    async def purge(self, inter: discord.Interaction, last_message_url: str):
        await inter.response.defer(ephemeral=True)
        ctx = await commands.Context.from_interaction(inter)
        last_message_url: discord.Message = await commands.MessageConverter().convert(ctx, last_message_url)

        channel = last_message_url.channel
        counter = 0
        async for message in channel.history(limit=None):
            counter += 1
            if message.id == last_message_url.id:
                break

        deleted = await channel.purge(limit=counter)
        await inter.followup.send(AdminMess.purged_messages(count=len(deleted), channel=channel.mention))

    # TODO remove with database counting of messages
    # @commands.has_permissions(administrator=True)
    # @commands.command(name="count", description="Count all messages from everyone")
    # async def message_count(self, ctx):
    #     member_ids = [member.id for member in ctx.guild.members]
    #     messages_count = {}
    #     headers = {'authorization': config.key}
    #     for ids in member_ids:
    #         r = requests.get(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/messages/search?author_id={ids}&include_nsfw=true', headers=headers)  # noqa: E501
    #         data = json.loads(r.text)
    #         username = ctx.guild.get_member(ids)

    #         messages_count.update({ids: data['total_results']})
    #         await ctx.send(f"**Jméno**= {username}; **ID**= {ids}; **počet zpráv**= {data['total_results']}") # noqa: E501
    #         # prevent rate limit
    #         time.sleep(2)

    #     with open(f"servers/{ctx.guild.name}/messages.json", 'w', encoding='utf-8') as f:
    #         json.dump(messages_count, f, ensure_ascii=False, indent=4)

    # @commands.has_permissions(administrator=True)
    # @commands.slash_command(name="history", description=AdminMess.channel_history_brief)
    # async def channel_history(
    #         self,
    #         inter,
    #         channel: discord.TextChannel,
    #         old_to_new: bool = commands.Param(default=True, description="Sort messages chronologically"),
    #         limit: int = commands.Param(default=None, description="Number of messages to retrieve")
    #         ):
    #     await inter.send(AdminMess.channel_history_retrieving_messages.format(channel.mention))
    #     messages = await channel.history(limit=limit, oldest_first=old_to_new).flatten()

    #     users = {}
    #     with open(f"{channel}_users.txt", "w") as file:
    #         for message in messages:
    #             users[message.author.id] = message.author.name

    #         for user_id, user_name in users.items():
    #             file.write(f"{user_id} | {user_name}\n")

    #     timezone = pytz.timezone('Europe/Prague')
    #     with open(f"{channel}_history.txt", "w") as file:
    #         for message in messages:
    #             utc_now = message.created_at
    #             time = utc_now.astimezone(timezone).strftime("%Y-%m-%d %H:%M:%S")
    #             content = message.content.replace("\n", " ")
    #             author = str(message.author.id).ljust(len(str(message.author.id)), " ")
    #             file.write(f"{time} | {author} | {content}\n")

    #     await inter.author.send(file=discord.File(f"{channel}_history.txt"))
    #     await inter.author.send(file=discord.File(f"{channel}_users.txt"))
    #     await inter.edit_original_message(AdminMess.channel_history_success.format(channel))

    #     if os.path.exists(f"{channel}_history.txt"):
    #         os.remove(f"{channel}_history.txt")
    #     if os.path.exists(f"{channel}_users.txt"):
    #         os.remove(f"{channel}_users.txt")

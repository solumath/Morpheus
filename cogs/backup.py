import asyncio
from disnake.ext import commands
import aiohttp
import disnake
import utility
from config.app_config import config
from config.messages import Messages


class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(utility.is_bot_admin)
    @commands.command(name="webhook", description=Messages.webhook_backup_brief)
    async def webhook_backup(self, ctx, rate=100):
        """use webhook to imitate users and backup whole channel history"""
        channel = self.bot.get_channel(config.bot_room)
        messages = await channel.history(limit=None, oldest_first=False).flatten()
        messages.reverse()
        msg = await ctx.send(f"• zpráv: {len(messages)}\n" + utility.create_bar(0, len(messages)))
        for index, message in enumerate(messages):
            async with aiohttp.ClientSession() as session:
                webhook = disnake.Webhook.from_url(config.webhook, session=session)
                if (index % 15 == 0):
                    await asyncio.sleep(30)
                if (index % rate == 0):
                    await msg.edit(
                        f"• zpráv: {len(messages)}\n• zpracovaných zpráv: {index+1}\n"
                        + utility.create_bar(index+1, len(messages))
                    )
                files_attached = []
                urls = ""
                embeds = []
                if message.is_system():
                    continue
                if message.attachments:
                    for attachment in message.attachments:
                        if attachment.size > 8388608:
                            urls += attachment.url
                            continue
                        else:
                            files_attached.append(await attachment.to_file())
                    if len(files_attached) > 1:
                        for file in files_attached:
                            await webhook.send(
                                message.content + f"\n{urls}",
                                username=message.author.name,
                                avatar_url=message.author.display_avatar.url,
                                file=file,
                                embeds=embeds
                            )
                        continue
                if message.stickers:
                    for sticker in message.stickers:
                        await webhook.send(
                            username=message.author.name,
                            avatar_url=message.author.display_avatar.url,
                            file=await sticker.to_file()
                        )
                    continue
                if message.embeds:
                    for embed in message.embeds:
                        if embed.type == "rich":
                            embeds = message.embeds
                await webhook.send(
                    message.content + f"\n{urls}",
                    username=message.author.name,
                    avatar_url=message.author.display_avatar.url,
                    files=files_attached,
                    embeds=embeds
                )

        await msg.edit(f"Úspěšné dokončení zálohy kanálu {channel.mention}.\n• zpráv: {len(messages)}")


def setup(bot):
    bot.add_cog(Backup(bot))

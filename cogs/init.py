from disnake.ext import commands

import os
import shutil
import json
from config import channels, messages

channels = channels.Channels
messages = messages.Messages

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        """setup folder for new server"""
        channel = self.bot.get_channel(channels.development)

        try:
            #----------------------Create dir-----------------------------
            if not (os.path.isdir(f"servers/{ctx.name}")):
                os.mkdir(f"servers/{ctx.name}")

            #----------------------Create replies-------------------------
            if not (os.path.isfile(f"servers/{ctx.name}/replies.json")):
                with open(f"servers/{ctx.name}/replies.json", "w") as f:
                    json.dump({"PR": "https://github.com/solumath/Morpheus"}, f, ensure_ascii=False, indent=4)

            print(messages.created_folder.format(ctx.name))
            await channel.send(messages.created_folder.format(ctx.name))

        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
            await channel.send(f"Error: {e.filename} - {e.strerror}.")

    @commands.Cog.listener()
    async def on_guild_remove(self, ctx):
        """remove folder of server"""
        channel = self.bot.get_channel(channels.development)

        try:
            if (os.path.isdir(f"servers/{ctx.name}")):
                shutil.rmtree(f"servers/{ctx.name}")
            print(messages.removed_folder.format(ctx.name))
            await channel.send(messages.removed_folder.format(ctx.name))

        except OSError as e:
            print(f"Error: {e.filename} - {e.strerror}.")
            await channel.send(f"Error: {e.filename} - {e.strerror}.")

def setup(bot):
    bot.add_cog(Init(bot))
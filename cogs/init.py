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

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="edit_config", description="Edits config file")
    async def edit_config(self, ctx, info_channel):
        print(info_channel[2:-1])
        with open(f"servers/{ctx.guild.name}/config.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            dict['joined'] = info_channel[2:-1]
            with open(f"servers/{ctx.guild.name}/config.json",'w', encoding='utf-8') as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)
            await ctx.send(f"Info channel byl změněn na kanál {info_channel}")

    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        """setup folder for new server"""
        channel = self.bot.get_channel(channels.development)

        try:
            #----------------------Create dir-----------------------------
            if not (os.path.isdir(f"servers/{ctx.name}")):
                os.mkdir(f"servers/{ctx.name}")
            
            #----------------------Create config-----------------------------
            if not (os.path.isdir(f"servers/{ctx.name}")):
                with open(f"servers/{ctx.name}/config.json", "w") as f:
                    json.dump({"joined": ""}, f, ensure_ascii=False, indent=4)

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
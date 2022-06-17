import disnake
from disnake.ext import commands

import os
import shutil
import json
from config.messages import Messages
from config.channels import Channels

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = ""

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="edit_config", description="Edits config file")
    async def edit_config(self, inter: disnake.ApplicationCommandInteraction, info_channel):
        with open(f"servers/{inter.guild.name}/config.json", 'r+', encoding='utf-8') as f:
            dict = json.load(f)
            dict['joined'] = info_channel[2:-1]
            with open(f"servers/{inter.guild.name}/config.json",'w', encoding='utf-8') as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)
            await inter.response.send_message(f"Info channel byl změněn na kanál {info_channel}")

    @commands.has_permissions(administrator=True)
    @commands.slash_command(name="manual_init", description="Initialize folders/files manually")
    async def manual_init(self, inter: disnake.ApplicationCommandInteraction):
        await self.create_files(inter)
        await inter.response.send_message(self.msg)

    @commands.Cog.listener("on_guild_join")
    async def create_files(self, inter: disnake.ApplicationCommandInteraction):
        """setup folder for new server"""
        channel = self.bot.get_channel(Channels.development)

        try:
            #----------------------Create dir-----------------------------
            if not (os.path.isdir(f"servers/{inter.guild.name}")):
                os.mkdir(f"servers/{inter.guild.name}")

            #----------------------Create config-----------------------------
            if not (os.path.isdir(f"servers/{inter.guild.name}")):
                with open(f"servers/{inter.guild.name}/config.json", "w") as f:
                    json.dump({"joined": ""}, f, ensure_ascii=False, indent=4)

            #----------------------Create replies-------------------------
            if not (os.path.isfile(f"servers/{inter.guild.name}/replies.json")):
                with open(f"servers/{inter.guild.name}/replies.json", "w") as f:
                    json.dump({"PR": "https://github.com/solumath/Morpheus"}, f, ensure_ascii=False, indent=4)

            self.msg = Messages.created_folder.format(inter.guild.name)
            print(self.msg)
            await channel.send(self.msg)

        except OSError as e:
            self.msg = Messages.filename_error.format(e.filename, e.strerror)
            print(self.msg)
            await channel.send(self.msg)

    @commands.Cog.listener("on_guild_remove")
    async def remove_files(self, inter: disnake.ApplicationCommandInteraction):
        """remove folder of server"""
        channel = self.bot.get_channel(Channels.development)

        try:
            if (os.path.isdir(f"servers/{inter.guild.name}")):
                shutil.rmtree(f"servers/{inter.guild.name}")

            self.msg = Messages.removed_folder.format(inter.guild.name)
            print(self.msg)
            await channel.send(self.msg)

        except OSError as e:
            self.msg = Messages.filename_error.format(e.filename, e.strerror)
            print(self.msg)
            await channel.send(self.msg)


def setup(bot):
    bot.add_cog(Init(bot))

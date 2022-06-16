from genericpath import isdir, isfile
import disnake
from disnake.ext import commands
import os

from config.messages import Messages
from config.channels import Channels

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unloadable_cogs = ["system"]


    @commands.is_owner()
    @commands.slash_command(name="cogs", description="Manipulate with cogs")
    async def cogs(self, inter):
        """slash commands for manipulating with extensions""" 
        pass

    @cogs.sub_command(name="load", description="Loads cog file")
    async def load(self, inter: disnake.ApplicationCommandInteraction, extension: str):
        try:
            self.bot.load_extension(f"cogs.{extension}")
            print(Messages.succes_load.format(extension))
            await inter.response.send_message(Messages.succes_load.format(extension))
        except Exception as e:
            await inter.response.send_message(f"Loading error\n`{e}`")

    @cogs.sub_command(name="unload", description="Unloads cog file")
    async def unload(self, inter: disnake.ApplicationCommandInteraction, extension: str):
        if extension in self.unloadable_cogs:
            await inter.response.send_message(Messages.not_loaded.format(extension))
            return

        try:
            self.bot.unload_extension(f"cogs.{extension}")
            print(Messages.succes_unload.format(extension))
            await inter.response.send_message(Messages.succes_unload.format(extension))
        except Exception as e:
            await inter.response.send_message(f"Unloading error\n`{e}`")

    @cogs.sub_command(name="reload", description="Reloads cog(s) file")
    async def rel(self, inter: disnake.ApplicationCommandInteraction, extension: str, all: bool = False):
        if all:
            channel = self.bot.get_channel(inter.channel.id)
            await inter.response.send_message("Reloading all cogs:")
            for extension in os.listdir("./cogs"):
                if extension.endswith(".py"):
                    try:
                        self.bot.reload_extension(f"cogs.{extension[:-3]}")
                        print(Messages.succes_reload.format(extension[:-3]))
                        await channel.send(Messages.succes_reload.format(extension[:-3]))
                    except Exception as e:
                        await channel.send(f"Reloading error\n`{e}`")
            await channel.send("Done")

        else:
            try:
                self.bot.reload_extension(f"cogs.{extension}")
                print(Messages.succes_reload.format(extension))
                await inter.response.send_message(Messages.succes_reload.format(extension))
            except Exception as e:
                await inter.response.send_message(f"Reloading error\n`{e}`")

    @cogs.sub_command(name="list", description="List of loaded cogs")
    async def list_cogs(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("\n".join([cog.lower() for cog in self.bot.cogs]))

    @load.autocomplete("extension")
    async def load_autocomp(self, inter: disnake.ApplicationCommandInteraction, user_input: str):
        all_cogs = []
        for name in os.listdir("./cogs"):
            filename = f"./cogs/{name}"
            if isfile(filename) and filename.endswith(".py"):
                all_cogs.append(name[:-3])
            
            if isdir(filename) and ("__init__.py" in os.listdir(filename)):
                all_cogs.append(name)
        
        loaded = [cog.lower() for cog in self.bot.cogs]
        cogs = list(set(all_cogs) - set(loaded))
        if cogs:
            return [cog for cog in cogs if user_input.lower() in cog]
        else:
            return ["All cogs loaded."]

    @unload.autocomplete("extension")
    @rel.autocomplete("extension")
    async def load_autocomp(self, inter: disnake.ApplicationCommandInteraction, user_input: str):
        cogs = [cog.lower() for cog in self.bot.cogs if user_input.lower() in cog.lower()]
        cogs.sort()
        return cogs


def setup(bot):
    bot.add_cog(System(bot))
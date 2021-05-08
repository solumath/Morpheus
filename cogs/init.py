import discord
from discord.ext import commands
from discord_slash import cog_ext
import os
import json

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="setupdir", description="setup folders for server")
    async def setupDir(self, ctx):
        """setup folder for new server"""
        #----------------------Create dir-----------------------------
        if not (os.path.isdir(f"servers")):
            os.mkdir(f"servers")
        if not (os.path.isdir(f"servers/{ctx.guild.name}")):
            os.mkdir(f"servers/{ctx.guild.name}")

        #----------------------Create replies-------------------------
        if not (os.path.isfile(f"servers/{ctx.guild.name}/replies.json")):
            with open(f"servers/{ctx.guild.name}/replies.json", "w") as f:
                json.dump({"PR": "https://github.com/solumath/KanekiBot"}, f, ensure_ascii=False, indent=4)

        #----------------------Create logs----------------------------
        if not (os.path.isdir(f"servers/{ctx.guild.name}/logs")):
            os.mkdir(f"servers/{ctx.guild.name}/logs")

def setup(bot):
    bot.add_cog(Init(bot))
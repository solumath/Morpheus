import disnake
from disnake.ext import commands

import os
import json

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="setupdir", description="setup folders for server")
    @commands.has_permissions(administrator=True)
    async def setupDir(self, ctx):
        await ctx.defer()
        """setup folder for new server"""
        #----------------------Create dir-----------------------------
        if not (os.path.isdir(f"servers")):
            os.mkdir(f"servers")
        if not (os.path.isdir(f"servers/{ctx.guild.name}")):
            os.mkdir(f"servers/{ctx.guild.name}")

        #----------------------Create replies-------------------------
        if not (os.path.isfile(f"servers/{ctx.guild.name}/replies.json")):
            with open(f"servers/{ctx.guild.name}/replies.json", "w") as f:
                json.dump({"PR": "https://github.com/solumath/Morpheus"}, f, ensure_ascii=False, indent=4)

        #----------------------Create logs----------------------------
        if not (os.path.isdir(f"servers/{ctx.guild.name}/logs")):
            os.mkdir(f"servers/{ctx.guild.name}/logs")
        await ctx.send("Setup done")

def setup(bot):
    bot.add_cog(Init(bot))
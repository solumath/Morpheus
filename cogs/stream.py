import discord
import random
from discord.ext import commands
import os
import subprocess
import datetime
import threading
import asyncio
from multiprocessing import Pool
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download(self, msg, output, link, start, duration):

        args = ["python3", "streamscript/yt_ddl.py", link, "-o", output, "-s", start, "-d", duration]
        p = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await p.communicate()

        if p.returncode == 0:
            await msg.edit(content=f"Successfully downloaded `{output}`")
        else:
            await msg.edit(content=f"Failed to download `{output}`\n\n```{(out+err).decode()}```")

    @commands.command(aliases=["dw","download","s"], usage="download <SUBJECT> <LINK> <START xx:xx> <DURATION h/m>")
    async def stream(self, ctx, subject, link, start, duration):
        """Download part of stream"""

        time = datetime.date.today()
        filename = f"{time}_{subject}.mp4"

        # strip <> just because someone can use it
        if link[0] == '<' and link[-1] == '>':
            link = link[1:-1]

        msg = await ctx.send(f"Downloading `{duration}` of `{link}` from {time} saving to `{filename}`...")

        asyncio.create_task(self.download(msg, filename, link, start, duration))


    @stream.error
    async def command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send(f"{ctx.command.usage} {ctx.author.mention}")

def setup(bot):
    bot.add_cog(Stream(bot))

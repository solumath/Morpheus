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

    async def download(self, ctx, args):
        await ctx.send("in thread")
        p = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await ctx.send("communicate")
        out, err = await p.communicate()
        out = out.decode("utf-8")
        print(f'retcode: {p.returncode}')
        print(f'stdout: {out}')
        print(f'stderr: {err}')
        await ctx.send(f"`Output: {out}`")

        if "Error" not in out:
            await ctx.send(f"Downloading was succesful")
        else:
            await ctx.send(f"Downloading failed")

    @commands.command(aliases=["dw","download","s"], usage="download <SUBJECT> <LINK> <START xx:xx> <DURATION h/m>")
    async def stream(self, ctx, subject, link, start, duration):
        """Download part of stream"""
        #upload file and remove

        await ctx.send("starting download")
        time = datetime.date.today()
        args = ["python3", "streamscript/yt_ddl.py", f"{link}", "-o", f"{time}_{subject}.mp4", "-s", f"{start}", "-d", f"{duration}"]
        asyncio.create_task(self.download(ctx, args))

    @stream.error
    async def command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send(f"{ctx.command.usage} {ctx.author.mention}")

def setup(bot):
    bot.add_cog(Stream(bot))
import discord
import random
from discord.ext import commands
import os
import subprocess
import datetime
import threading
import asyncio
import env
from multiprocessing import Pool
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

time = datetime.date.today()
gauth = GoogleAuth()           
drive = GoogleDrive(gauth) 

class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download(self, msg, output, link, start, duration, subject, ctx):
        """Thread function for downloading stream and uploading to drive"""
        args = ["python3", "streamscript/yt_ddl.py", link, "-o", output, "-s", start, "-d", duration]
        p = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await p.communicate()

        if p.returncode == 0:
            await msg.edit(content=f"Successfully downloaded `{output}`")
        else:
            await msg.edit(content=f"Failed to download `{output}`\n\n```{(out+err).decode()}```")

        # TODO semaphor or synchronization so multiple downloads can run in the background
        # TODO if name of file is same, update file instead of uploading another one
        
        # check for folder with name subject
        folders = drive.ListFile({'q': f"title='{subject}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

        try:
            # check if folder was found if not create folder and upload to it
            if folders != []:
                for folder in folders:
                    if folder.get("title") == subject:
                        gfile = drive.CreateFile({'title': output,'parents': [{'id': folder['id']}]})
                        gfile.Upload()
                        os.remove(output)
                        await ctx.send("File successfully uploaded")

            else:
                new_folder = drive.CreateFile({'title': subject,"parents":[{'id': env.DRIVE_ID}],'mimeType':"application/vnd.google-apps.folder"})
                new_folder.Upload()
                gfile = drive.CreateFile({'title': output,'parents': [{'id': new_folder['id']}]})
                gfile.Upload()
                await ctx.send("File successfully uploaded")
                os.remove(output)
        except Exception:
            await ctx.send(Exception)
        
    @commands.command(aliases=["dw","download","s"], usage="download <SUBJECT> <LINK> <START xx:xx> <DURATION h/m>")
    async def stream(self, ctx, subject, link, start, duration):
        """Download part of stream"""
        subject = (subject.lower()).replace(" ", "_")
        filename = f"{time}_{subject}.mp4"

        # strip <> just because someone can use it
        if link[0] == '<' and link[-1] == '>':
            link = link[1:-1]

        msg = await ctx.send(f"Downloading `{duration}` of `{link}` from {time} saving to `{filename}`...")

        asyncio.create_task(self.download(msg, filename, link, start, duration, subject, ctx))


    @stream.error
    async def command_error(self, ctx, error):
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send(f"{ctx.command.usage} {ctx.author.mention}")

def setup(bot):
    bot.add_cog(Stream(bot))
from disnake.ext import commands

import datetime
import asyncio
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

time = datetime.date.today()
gauth = GoogleAuth()
drive = GoogleDrive(gauth)


class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def download(self, inter, filename, link, start, duration, subject):
        """Thread function for downloading stream and uploading to drive"""
        args = ["python3", "streamscript/yt_ddl.py", link, "-o",
                filename, "-s", start, "-d", duration]
        p = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
        out, err = await p.communicate()

        if p.returncode == 0:
            await inter.edit_original_message(content=f"Successfully downloaded `{filename}`")
        else:
            await inter.edit_original_message(content=f"Failed to download `{filename}`\n\n```{(out+err).decode()}```")

        # TODO semaphor or synchronization so multiple downloads can run in the background
        # TODO if name of file is same, update file instead of uploading another one
        # TODO rewrite upload (cant upload file bigger than 100MB with pydrive)

    @commands.slash_command(name="stream",
                            description="download <SUBJECT> <LINK> <START xx:xx> <DURATION h/m>")
    async def stream(self, inter, subject, link, start, duration):
        """Download part of stream"""
        subject = (subject.lower()).replace(" ", "_")
        filename = f"{time}_{subject}.mp4"

        # strip <> just because someone can use it
        if link[0] == '<' and link[-1] == '>':
            link = link[1:-1]

        await inter.send(f"Downloading `{duration}` of `{link}` from {time} saving to `{filename}`...")

        asyncio.create_task(self.download(inter, filename, link, start, duration, subject))


def setup(bot):
    bot.add_cog(Stream(bot))

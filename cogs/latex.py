import aiohttp
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import io
import urllib
from PIL import Image

PNG_HEADER = b'\x89PNG\r\n\x1a\n'

class Latex(commands.Cog):
    @cog_ext.cog_slash(name="latex", description="Vykreslí LaTeX výraz")
    async def latex(self, ctx, *, equation):
        eq = urllib.parse.quote(equation)
        imgURL = f"http://www.sciweavers.org/tex2img.php?eq={eq}&fc=White&im=png&fs=25&edit=0"
        async with aiohttp.ClientSession() as session:
            async with session.get(imgURL) as resp:
                if resp.status != 200:
                    return await ctx.send("Could not get image.")
                data = await resp.read()
                if not data.startswith(PNG_HEADER):
                    return await ctx.send("Could not get image.")
                datastream = io.BytesIO(data)
                await ctx.send(file=discord.File(datastream, "latex.png"))


def setup(bot):
    bot.add_cog(Latex(bot))
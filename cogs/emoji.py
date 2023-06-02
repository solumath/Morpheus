import io
import zipfile

import disnake
from disnake.ext import commands

from config.messages import Messages


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="emoji_download", description=Messages.emoji_download_brief)
    async def emoji_download(self, inter: disnake.ApplicationCommandInteraction):
        """Get all emojis from server"""
        await inter.response.defer()
        emojis = await inter.guild.fetch_emojis()

        with zipfile.ZipFile("emojis.zip", "w") as zip_file:
            for emoji in emojis:
                with io.BytesIO() as image_binary:
                    if emoji.animated:
                        emoji_name = f"{emoji.name}.gif"
                    else:
                        emoji_name = f"{emoji.name}.png"
                    await emoji.save(image_binary)
                    zip_file.writestr(emoji_name, image_binary.getvalue())

        await inter.send(file=disnake.File("emojis.zip"))


def setup(bot):
    bot.add_cog(Emoji(bot))

from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw

from cogs.base import Base
from custom.cooldowns import default_cooldown

from .messages import PetMess


class Pet(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @default_cooldown()
    @app_commands.command(name="pet", description=PetMess.pet_brief)
    async def pet(self, inter: discord.Interaction, user: discord.User = None):
        user = user or inter.user
        if not user.avatar:
            await inter.response.send_message(PetMess.pet_unsupported_avatar)
            return

        avatar = await user.display_avatar.read()
        avatarFull = Image.open(BytesIO(avatar))

        frames = []
        deformWidth = [-1, -2, 1, 2, 1]
        deformHeight = [4, 3, 1, 1, -4]
        width = 80
        height = 80

        for i in range(5):
            frame = Image.new("RGBA", (112, 112), (255, 255, 255, 1))
            hand = Image.open(f"cogs/pet/images/{i}.png")
            width = width - deformWidth[i]
            height = height - deformHeight[i]
            avatar = avatarFull.resize((width, height))
            avatarMask = Image.new("1", avatar.size, 0)
            draw = ImageDraw.Draw(avatarMask)
            draw.ellipse((0, 0) + avatar.size, fill=255)
            avatar.putalpha(avatarMask)

            frame.paste(avatar, (112 - width, 112 - height), avatar)
            frame.paste(hand, (0, 0), hand)
            frames.append(frame)

        with BytesIO() as image_binary:
            frames[0].save(
                image_binary,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                duration=40,
                loop=0,
                transparency=0,
                disposal=2,
                optimize=False,
            )
            image_binary.seek(0)
            await inter.response.send_message(file=discord.File(fp=image_binary, filename="pet.gif"))

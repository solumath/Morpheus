import discord

from .messages import NasaMess


def create_nasa_embed(response: dict) -> discord.Embed:
    """
    Create embed for NASA API response
    """
    embed = discord.Embed(title=response["title"], url=NasaMess.nasa_url, color=discord.Color.blurple())
    embed.set_image(url=response["hdurl"])
    embed.add_field(name="Explanation", value=response["explanation"], inline=False)
    return embed

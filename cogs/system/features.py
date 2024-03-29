import os
from os.path import isdir, isfile

import discord
from discord.ext import commands

from config.app_config import config
from utils import utils

from .messages import SystemMess


def get_all_cogs() -> list[tuple[str, str]]:
    """get all cog modules"""
    path = "./cogs"
    all_cogs = []

    for name in os.listdir(path):
        if not isdir(f"{path}/{name}"):
            continue

        if not isfile(f"{path}/{name}/__init__.py"):
            continue

        all_cogs.append((name, f"{path}/{name}"))

    return sorted(all_cogs)


async def split_cogs() -> list[tuple[str, str]]:
    """Slices dictionary of all cogs to chunks for select."""
    cog_pairs = get_all_cogs()
    all_cogs = []
    pairs_count = len(cog_pairs)
    chunk_size = 25

    for i in range(0, len(cog_pairs), chunk_size):
        pairs = cog_pairs[i : min(i + chunk_size, pairs_count)]
        all_cogs.append(pairs)

    return all_cogs


def create_embed(bot: commands.Bot) -> discord.Embed:
    embed = discord.Embed(title=SystemMess.embed_title, colour=discord.Color.yellow())
    bot_cogs = [cog.lower() for cog in bot.cogs]
    cogs = get_all_cogs()
    cog_count = len(cogs)

    cog_loaded = []
    cog_unloaded = []
    for cog_name, _ in cogs:
        if cog_name in bot_cogs:
            if cog_name not in config.extensions:
                cog_loaded.append(f"✅ **{cog_name.title()}**\n\n")
            else:
                cog_loaded.append(f"✅ {cog_name.title()}\n\n")
        else:
            if cog_name in config.extensions:
                cog_unloaded.append(f"❌ **{cog_name.title()}**\n\n")
            else:
                cog_unloaded.append(f"❌ {cog_name.title()}\n\n")

    loaded_count = len(cog_loaded)
    unloaded_count = len(cog_unloaded)

    embed.description = SystemMess.embed_description(loaded=loaded_count, unloaded=unloaded_count, all=cog_count)

    chunks_count = 2 if cog_count <= 20 else 3

    loaded_chunks = utils.split(cog_loaded, chunks_count)
    unloaded_chunks = utils.split(cog_unloaded, chunks_count)

    for loaded_chunk in loaded_chunks:
        embed.add_field(name="\u200b", value="".join(loaded_chunk), inline=True)

    # separator
    if unloaded_chunks:
        embed.add_field(name="\u200b", value="", inline=False)

    for unloaded_chunk in unloaded_chunks:
        embed.add_field(name="\u200b", value="".join(unloaded_chunk), inline=True)

    embed.set_footer(text=SystemMess.override)
    return embed

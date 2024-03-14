import os
from os.path import isdir, isfile


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

import discord


def get_emoji_count(guild: discord.Guild) -> tuple[int, int]:
    """Get count of all emojis from Guild"""
    emojis = 0
    animated_emojis = 0
    for emoji in guild.emojis:
        if emoji.animated:
            animated_emojis += 1
        else:
            emojis += 1

    return emojis, animated_emojis

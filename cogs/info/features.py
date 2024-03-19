import discord


def get_emoji_count(guild: discord.Guild) -> int:
    """Get count of all emojis from Guild"""
    emojis, animated_emojis = 0
    for emoji in guild.emojis:
        if emoji.animated:
            animated_emojis += 1
        else:
            emojis += 1

    return emojis, animated_emojis

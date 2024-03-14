from typing import Optional

import discord


async def get_or_fetch_user(bot, user_id: int) -> Optional[discord.User]:
    """
    Tries to get the user from the cache. If fails, it tries to
    fetch the user from the API.

    Parameters
    ----------
    user_id: :class:`int`
        The ID to search for.

    Returns
    -------
    Optional[:class:`~discord.User`]
        The user with the given ID, or ``None`` if not found and ``strict`` is set to ``False``.
    """
    user = bot.get_user(user_id)
    if user is not None:
        return user
    try:
        user = await bot.fetch_user(user_id)
    except Exception:
        return None
    return user

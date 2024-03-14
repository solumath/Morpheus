from typing import Union

import discord
from discord.ext import commands

from config.app_config import config

from .custom_errors import NotAdminError


def is_bot_admin(raise_exception: bool = True):
    """@Decorator that checks if the user is a bot admin.

    Parameters
    -----------
    raise_exception : `bool`
        If True, raises `NotAdminError`. If False, returns `bool`.

    Raises
    -------
    NotAdminError
        If `raise_exception` is True and the user is not a bot admin.

    Returns
    --------
    `bool`
        True if the user is a bot admin, False otherwise.
    """

    async def predicate(ctx: Union[commands.Context, discord.Interaction]):
        if ctx.author.id in config.admin_ids:
            return True

        if not raise_exception:
            return False
        raise NotAdminError

    return commands.check(predicate)

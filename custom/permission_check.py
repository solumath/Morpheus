import discord
from discord.ext import commands

from config.app_config import config

from .custom_errors import NotAdminError


def is_bot_admin(ctx: commands.Context | discord.Interaction, raise_exception: bool = True):
    """Checks if the user is a bot admin.

    Parameters
    -----------
    ctx : `commands.Context` | `discord.Interaction`
        The context of the command.
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
    author_id = ctx.user.id if isinstance(ctx, discord.Interaction) else ctx.author.id
    if author_id in config.admin_ids:
        return True

    if not raise_exception:
        return False
    raise NotAdminError

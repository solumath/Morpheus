from discord.ext import commands

from cogs.bookmark.buttons import BookmarkView
from cogs.roles.dropdowns import ChannelsSelectView, RolesSelectView


def instantiate_views(bot: commands.Bot) -> None:
    """
    Instantiate and add permanent views to the bot.

    Parameters
    ----------
    bot: :clas:`commands.Bot`
        The bot instance to which the views will be added.

    Returns
    -------
    None
    """
    views = {RolesSelectView, ChannelsSelectView, BookmarkView}
    for view in views:
        bot.add_view(view(bot))

from discord.ext import commands

from cogs.bookmark.buttons import BookmarkView
from cogs.roles.dropdowns import ChannelsSelectView, RolesSelectView


def init_views(bot: commands.Bot) -> None:
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
    bot.add_view(RolesSelectView(bot))
    bot.add_view(ChannelsSelectView(bot))
    bot.add_view(BookmarkView())

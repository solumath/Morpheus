from __future__ import annotations

from typing import TYPE_CHECKING

from cogs.bookmark.buttons import BookmarkView
from cogs.roles.dropdowns import ChannelsSelectView, RolesSelectView

if TYPE_CHECKING:
    from morpheus import Morpheus


def init_views(bot: Morpheus) -> None:
    """
    Instantiate and add permanent views to the bot.

    Parameters
    ----------
    bot: :clas:`morpheus.Morpheus`
        The bot instance to which the views will be added.

    Returns
    -------
    None
    """
    bot.add_view(RolesSelectView(bot))
    bot.add_view(ChannelsSelectView(bot))
    bot.add_view(BookmarkView())

from cogs.bookmark.buttons import BookmarkView
from cogs.roles.dropdowns import ChannelsSelectView, RolesSelectView


def instantiate_views(bot):
    views = {RolesSelectView, ChannelsSelectView, BookmarkView}
    for view in views:
        bot.add_view(view(bot))

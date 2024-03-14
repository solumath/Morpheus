from config.messages import GlobalMessages


class AdminMess(GlobalMessages):
    emoji_brief = "Group of commands for getting emojis"
    get_emojis_brief = "Download all emojis and send them as emojis.zip"
    get_emoji_brief = "Show emoji in full size"
    invalid_emoji = "Invalid format of emoji"

    purge_brief = "Delete all messages to the specified message(included)"
    purged_messages = "Deleted {count} messages in channel {channel}"

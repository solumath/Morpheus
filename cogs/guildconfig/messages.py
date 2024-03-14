from config.messages import GlobalMessages


class GuildConfigMess(GlobalMessages):
    info_channel_set = "Info channel set to {info_channel}"

    edit_config_brief = "Edit guild config"
    add_reply_brief = "Add autoreply for the server"
    rem_reply_brief = "Remove autoreply for the server"
    reply_exists = "Reply for `{key}` already exists"
    reply_added = "Reply for `{key}` added"
    reply_removed = "Reply for `{key}` removed"
    reply_not_found = "Reply for `{key}` not found"

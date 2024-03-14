from config.messages import GlobalMessages


class CustomMess(GlobalMessages):
    # PERMISSION CHECK
    bot_admin_only = "This command can be used only by BOT Admins."

    # CUSTOM ERRORS
    not_enough_perms = "You do not posses enough strength to use this force."
    api_error = "Could not reach the API\n{error}"
    invalid_time_format = "Invalid time format.\n{time_format}."

from discord import app_commands
from discord.ext import commands

from custom.messages import CustomMess


class InvalidTime(app_commands.CheckFailure, commands.CommandError):
    """An error indicating that the time format is invalid."""

    def __init__(self, time_format: str) -> None:
        self.message = CustomMess.invalid_time_format(time_format=time_format)


class ApiError(app_commands.CheckFailure, commands.CommandError):
    """An error indicating that the api returned invalid status."""

    def __init__(self, error: str) -> None:
        self.message = CustomMess.api_error(error=error)


class NotAdminError(app_commands.CheckFailure, commands.CommandError):
    """An error indicating that a user doesn't have permissions to use
    a command that is available only to admins of bot.
    """

    def __init__(self) -> None:
        self.message = CustomMess.bot_admin_only

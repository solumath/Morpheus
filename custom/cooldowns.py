from typing import Union

from discord import app_commands
from discord.ext import commands

from custom.enums import CooldownType


def short_cooldown():
    """@Decorator that adds a cooldown to a command.

    5x/20s"""
    rate = 5
    per = 20.0

    def decorator(func: Union[commands.Command, app_commands.Command]):
        if isinstance(func, commands.Command):
            return commands.cooldown(rate=rate, per=per, type=CooldownType.user)(func)
        else:
            return app_commands.checks.cooldown(rate=rate, per=per, key=CooldownType.user)(func)

    return decorator


def default_cooldown():
    """@Decorator that adds a cooldown to a command.

    5x/30s
    """
    rate = 5
    per = 30.0

    def decorator(func: Union[commands.Command, app_commands.Command]):
        if isinstance(func, commands.Command):
            return commands.cooldown(rate=rate, per=per, type=CooldownType.user)(func)
        else:
            return app_commands.checks.cooldown(rate=rate, per=per, key=CooldownType.user)(func)

    return decorator


def long_cooldown():
    """@Decorator that adds a cooldown to a command.

    1x/20s"""
    rate = 1
    per = 20.0

    def decorator(func: Union[commands.Command, app_commands.Command]):
        if isinstance(func, commands.Command):
            return commands.cooldown(rate=rate, per=per, type=CooldownType.user)(func)
        else:
            return app_commands.checks.cooldown(rate=rate, per=per, key=CooldownType.user)(func)

    return decorator


def custom_cooldown(rate: int, per: float, type: CooldownType = CooldownType.user):
    """@Decorator that adds a cooldown to a command.

    rate: int
        How many times a command can be used before being put on cooldown.
    per: float
        How many seconds a command is put on cooldown for.
    """

    def decorator(func: Union[commands.Command, app_commands.Command]):
        if isinstance(func, commands.Command):
            return commands.cooldown(rate=rate, per=per, type=type)(func)
        else:
            return app_commands.checks.cooldown(rate=rate, per=per, key=type)(func)

    return decorator

from .guild_logger import GuildLogger


class TopLogger:
    def __init__(self):
        self.guild_loggers = {}

    def get_guild_logger(self, guild_id) -> GuildLogger:
        if guild_id not in self.guild_loggers:
            self.guild_loggers[guild_id] = GuildLogger(guild_id)
        return self.guild_loggers[guild_id]


top_logger = TopLogger()

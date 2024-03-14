import logging
import os
from logging.handlers import TimedRotatingFileHandler


def namer(name):
    """define log file name"""
    base_filename, ext, date = name.split(".")
    return f"{base_filename}.{date}.{ext}"


class GuildLogger:
    def __init__(self, guild_id):
        self.guild_id = guild_id

        self._formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        self.dir_path = f"logs/{self.guild_id}"

        self.message_logger = logging.Logger(f"message_logger_{self.guild_id}")
        self._message_handler = self._init_file_handler("messages")
        self._message_handler.setFormatter(self._formatter)
        self._message_handler.namer = namer
        self.message_logger.addHandler(self._message_handler)

        self.command_logger = logging.Logger(f"command_logger_{self.guild_id}")
        self._command_handler = self._init_file_handler("commands")
        self._command_handler.setFormatter(self._formatter)
        self._command_handler.namer = namer
        self.command_logger.addHandler(self._command_handler)

        self.reaction_logger = logging.Logger(f"reaction_logger_{self.guild_id}")
        self._reaction_handler = self._init_file_handler("reactions")
        self._reaction_handler.setFormatter(self._formatter)
        self._reaction_handler.namer = namer
        self.reaction_logger.addHandler(self._reaction_handler)

    def __del__(self):
        self.message_logger.removeHandler(self._message_handler)
        self.command_logger.removeHandler(self._command_handler)
        self.reaction_logger.removeHandler(self._reaction_handler)

        self._message_handler.close()
        self._command_handler.close()
        self._reaction_handler.close()

    def _init_file_handler(self, dir_name):
        dir_path = f"{self.dir_path}/{dir_name}"
        os.makedirs(dir_path, exist_ok=True)

        return TimedRotatingFileHandler(
            filename=f"{dir_path}/current.log",
            when="midnight",
            interval=1,
            encoding="utf-8",
            backupCount=365,
        )

import logging


class LoggerLeveles:
    Message = 21
    Reaction = 22
    Edit = 23
    Delete = 24
    Command = 25

    @staticmethod
    def add_level_names():
        logging.addLevelName(LoggerLeveles.Message, "MESSAGE")
        logging.addLevelName(LoggerLeveles.Reaction, "REACTION")
        logging.addLevelName(LoggerLeveles.Edit, "EDIT")
        logging.addLevelName(LoggerLeveles.Delete, "DELETE")
        logging.addLevelName(LoggerLeveles.Command, "COMMAND")

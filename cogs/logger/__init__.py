import logging
from logging.handlers import TimedRotatingFileHandler

from cogs.logger.logger import Logger

logger = logging.getLogger()
logger.setLevel(logging.INFO)
_handler = TimedRotatingFileHandler(filename=f"servers/logs/L", when="midnight", interval=1, encoding='utf-8', backupCount=31)
_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
_handler.suffix = "%d.%m.%Y.log"
logger.addHandler(_handler)

logging.addLevelName(21, "MSG")
logging.addLevelName(22, "REACT")
logging.addLevelName(23, "EDIT")
logging.addLevelName(24, "DEL")
logging.addLevelName(25, "COMM")

def setup(bot):
    bot.add_cog(Logger(bot, logger))

def teardown(_):
    logger.removeHandler(_handler)
    _handler.close()

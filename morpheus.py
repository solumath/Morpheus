import logging
import os
import platform

import discord
import git
import wavelink
from discord.ext import commands

from config.app_config import config
from custom.views import instantiate_views
from database import database_init


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="?", intents=discord.Intents.all())
        self.bot_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
        self.bot_formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")

        discord.utils.setup_logging(handler=self.bot_handler, formatter=self.bot_formatter)

    async def setup_hook(self) -> None:
        # initialize database
        database_init.init_db()
        logging.info("Database initialized")

        # connect to lavalink
        port = os.environ.get("SERVER_PORT", 2333)
        password = os.environ.get("LAVALINK_SERVER_PASSWORD", "youshallnotpass")
        nodes = [wavelink.Node(uri=f"ws://lavalink:{port}", password=password)]
        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=None)

        # load cogs
        await self.init_cogs()

        # add views
        instantiate_views(self)

        # get bot data
        await bot.application_info()

    async def on_ready(self) -> None:
        synced = await self.tree.sync()
        ready_string = f"Logged in as {self.user.mention} | {self.user.id}\n"
        ready_string += f"Python {platform.python_version()}\n"
        ready_string += f"discord.py {discord.__version__}\n"
        ready_string += f"Synced {len(synced)} commands"

        # set status for bot
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        await bot.change_presence(activity=discord.Game(f"On commit {sha[:7]}"))
        bot_room: discord.TextChannel = bot.get_channel(config.bot_dev_channel)
        if bot_room is not None:
            await bot_room.send(ready_string)

        logging.info(ready_string)

    async def init_cogs(self) -> None:
        """Loads all cogs from the cogs folder"""
        for cog in config.extensions:
            await bot.load_extension(f"cogs.{cog}")
            logging.info(f"Loaded {cog}")


bot: Bot = Bot()

bot.run(config.key)

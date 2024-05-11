"""
To automatically create table, import the class
"""

from database import database

from .guild import GuildDB, GuildPhraseDB  # noqa: F401
from .voice import PlaylistDB  # noqa: F401


async def init_db():
    async with database.engine.begin() as conn:
        # await conn.run_sync(database.base.metadata.drop_all)
        await conn.run_sync(database.base.metadata.create_all)

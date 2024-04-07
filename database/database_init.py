"""
To automatically create table, import the class
"""

from database import database, session

from .guild import GuildDB, GuildPhraseDB  # noqa: F401


def init_db(commit: bool = True):
    # database.base.metadata.drop_all(database.db)
    database.base.metadata.create_all(database.db)

    if commit:
        session.commit()

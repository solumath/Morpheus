from __future__ import annotations

import hashlib
from typing import Optional

from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database import database, session


class GuildDB(database.base):
    __tablename__ = "guild"

    id = Column(String, primary_key=True)
    phrases = relationship("GuildPhraseDB", back_populates="guild", cascade="all, delete", collection_class=set)
    info_channel_id = Column(String, nullable=True)

    @property
    def phrases_dict(self) -> dict[str, str]:
        return {phrase.key: phrase.value for phrase in self.phrases}

    @classmethod
    def get_guild(cls, guild_id: str) -> GuildDB:
        guild = session.query(cls).get(str(guild_id))
        if not guild:
            cls.add_guild(str(guild_id))
            guild = session.query(cls).get(str(guild_id))
        return guild

    @classmethod
    def add_guild(cls, guild_id: str):
        guild = cls(id=str(guild_id))
        session.add(guild)
        session.commit()

    def set_info_channel(self, channel_id: str):
        self.info_channel_id = str(channel_id)
        session.commit()

    @classmethod
    def get_info_channel(cls, guild_id: str) -> Optional[str]:
        guild = session.query(cls).get(str(guild_id))
        info_channel = guild.info_channel_id if guild.info_channel_id else None
        return info_channel


class GuildPhraseDB(database.base):
    __tablename__ = "guild_phrase"

    # unique key per guild
    __table_args__ = (UniqueConstraint("guild_id", "hash_key"),)

    hash_key = Column(String, primary_key=True)
    key = Column(String, nullable=False)
    guild_id = Column(ForeignKey("guild.id"), nullable=False)
    guild = relationship("GuildDB", back_populates="phrases")
    value = Column(String, nullable=False)

    @classmethod
    def create_hash_key(cls, key) -> str:
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return hashed_key

    @classmethod
    def get_phrase(cls, guild_id: str, key: str) -> Optional[GuildPhraseDB]:
        phrase = session.query(cls).filter_by(guild_id=str(guild_id), key=str(key)).first()
        return phrase

    @classmethod
    def add_phrase(cls, guild_id: str, key: str, value: str) -> Optional[GuildPhraseDB]:
        phrase = cls.get_phrase(str(guild_id), str(key))
        if phrase:
            return None

        hash_key = cls.create_hash_key(key)
        phrase = cls(guild_id=str(guild_id), key=str(key), hash_key=hash_key, value=str(value))
        session.add(phrase)
        session.commit()
        return phrase

    @classmethod
    def remove_phrase(cls, guild_id: str, key: str) -> Optional[GuildPhraseDB]:
        phrase = cls.get_phrase(str(guild_id), str(key))
        if not phrase:
            return None

        session.delete(phrase)
        session.commit()
        return phrase

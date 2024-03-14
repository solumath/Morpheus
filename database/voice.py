from __future__ import annotations

from sqlalchemy import Column, Integer, String, UniqueConstraint

from database import database, session


class PlaylistDB(database.base):
    __tablename__ = "playlist"

    __table_args__ = (UniqueConstraint("guild_id", "name"),)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    guild_id = Column(String, nullable=False)
    author_id = Column(String, nullable=False)

    @classmethod
    def add_playlist(cls, guild_id: str, author_id: str, name: str, url: str) -> PlaylistDB | None:
        if cls.get_playlist(guild_id, name):
            return
        playlist = cls(guild_id=str(guild_id), author_id=str(author_id), name=str(name), url=str(url))
        session.add(playlist)
        session.commit()
        return playlist

    @classmethod
    def remove_playlist(cls, guild_id: str, author_id: str, name: str) -> PlaylistDB | None:
        if cls.author_id != str(author_id):
            return
        playlist = session.query(cls).filter_by(guild_id=str(guild_id), name=str(name)).first()
        session.delete(playlist)
        session.commit()
        return playlist

    @classmethod
    def get_playlist(cls, guild_id: str, name: str) -> PlaylistDB:
        playlist = session.query(cls).filter_by(guild_id=str(guild_id), name=str(name)).first()
        return playlist.url

    @classmethod
    def get_playlists(cls, guild_id: str) -> list[PlaylistDB]:
        playlists = session.query(cls).filter_by(guild_id=str(guild_id)).all()
        return playlists

    @classmethod
    def get_guilds(cls) -> list[str]:
        guilds = session.query(cls.guild_id).distinct()
        return [guild[0] for guild in guilds]

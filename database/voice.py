from __future__ import annotations

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database import database, session


class PlaylistDB(database.base):
    __tablename__ = "playlist"

    __table_args__ = (UniqueConstraint("name", "author_id", "guild_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    guild_id: Mapped[str] = mapped_column(nullable=True)  # if None, it's a global playlist
    author_id: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    def get(cls, playlist_id: str) -> PlaylistDB | None:
        return session.query(cls).get(playlist_id)

    @classmethod
    def add_playlist(cls, guild_id: str | None, author_id: str, name: str, url: str) -> PlaylistDB | None:
        if cls.get_playlist(guild_id, author_id, name):
            return None

        playlist = cls(guild_id=guild_id, author_id=author_id, name=name, url=url)
        session.add(playlist)
        session.commit()
        return playlist

    @classmethod
    def remove_playlist(cls, inter_author_id: str, playlist_id: str) -> PlaylistDB | None:
        if inter_author_id != cls.author_id:
            return None

        playlist = session.query(cls).get(playlist_id)

        session.delete(playlist)
        session.commit()
        return playlist

    @classmethod
    def get_playlist(cls, guild_id: str | None, author_id: str, name: str) -> str | None:
        guild_id = None if guild_id == "None" else guild_id
        playlist = session.query(cls).filter_by(guild_id=guild_id, author_id=author_id, name=name).first()
        if playlist:
            return playlist.url

        return None

    @classmethod
    def get_author_playlists(cls, author_id: str) -> list[PlaylistDB]:
        return session.query(cls).filter_by(author_id=author_id).order_by(cls.name).all()

    @classmethod
    def get_available_playlists(cls, guild_id: str, author_id: str) -> list[PlaylistDB]:
        my_playlists = cls.get_author_playlists(author_id)
        guild_playlists = (
            session.query(cls).filter(cls.author_id != author_id, cls.guild_id == guild_id).order_by(cls.name).all()
        )
        return [*my_playlists, *guild_playlists]

    @classmethod
    def get_guilds(cls) -> list[str]:
        guilds = session.query(cls.guild_id).distinct()
        return [guild[0] for guild in guilds]

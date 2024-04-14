from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, cast

import discord
import wavelink

if TYPE_CHECKING:
    # prevent circular import
    from . import views

from utils.embed_utils import PaginationView

from .messages import VoiceMess


class Home:
    def __init__(self, channel: discord.TextChannel, voice_channel: discord.VoiceChannel):
        self.channel = channel
        self.voice_channel = voice_channel


class WavelinkPlayer(wavelink.Player):
    home: Home
    view: views.VoiceView
    message: discord.Message


class VoiceFeatures:
    @classmethod
    async def play(cls, inter: discord.Interaction, query: str, place: int = None) -> None:
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)

        if not player:
            try:
                player: WavelinkPlayer = await inter.user.voice.channel.connect(cls=WavelinkPlayer)
            except AttributeError:
                await inter.response.send_message(VoiceMess.join_channel, ephemeral=True)
                return
            except discord.ClientException:
                await inter.response.send_message(VoiceMess.unable_to_join)
                return

        if player.autoplay == wavelink.AutoPlayMode.disabled:
            player.autoplay = wavelink.AutoPlayMode.partial

        place = place - 1 if place else None  # make it 0 based index

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = Home(inter.channel, inter.guild.voice_client.channel)
        elif (player.home.channel != inter.channel) and (player.home.voice_chanel != inter.channel):
            await inter.response.send_message(VoiceMess.home_channel(channel=player.home.channel.mention))
            return

        # This will handle fetching Tracks and Playlists...
        # Seed the doc strings for more information on this method...
        # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
        # Defaults to YouTube for non URL based queries...
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await inter.response.send_message(VoiceMess.no_track_found(user=inter.user.mention), ephemeral=True)
            return

        if isinstance(tracks, wavelink.Playlist):
            # tracks is a playlist...
            if place or place == 0:
                await inter.response.send_message(VoiceMess.playlist_place, ephemeral=True)
                return
            for track in tracks:
                track.extras = {"requester": inter.user.id}
            added: int = await player.queue.put_wait(tracks)
            await inter.response.send_message(
                f"[Added the playlist **`{tracks.name}`** ({added} songs) to the queue.]({query})"
            )
        else:
            track: wavelink.Playable = tracks[0]
            track.extras = {"requester": inter.user.id}
            if place or place == 0:
                player.queue.put_at(place, track)
            else:
                await player.queue.put_wait(track)
            await inter.response.send_message(f"[Added **`{track}`** to the queue.]({track.uri})")

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=30)

    @classmethod
    def create_embed(
        cls, title: str = None, description: str = None, color: discord.Color = discord.Color.dark_blue()
    ) -> discord.Embed:
        """Create an embed."""
        embed = discord.Embed(title=title, description=description, color=color)
        return embed

    @classmethod
    def now_playing_embed(
        cls, player: WavelinkPlayer, author: discord.User, recommended: bool = False
    ) -> discord.Embed:
        """Create an embed for the now playing message."""
        current_track = player.current
        description = VoiceMess.current_track(playing_emoji=VoiceMess.playing_emoji, current_track=current_track)

        embed = cls.create_embed(description=description)
        embed.set_author(name="NOW PLAYING", icon_url=author.display_avatar.url)

        if recommended:
            embed.add_field(name="Autoplay via", value=f"`{current_track.source}`", inline=True)
        else:
            embed.add_field(name="Requested by", value=author.mention, inline=True)

        embed.add_field(name="Song by", value=f"`{current_track.author}`", inline=True)

        try:
            length = timedelta(milliseconds=current_track.length)
            length = str(length).split(".")[0]  # remove milliseconds
            embed.add_field(name="Duration", value=f"`> {length}`", inline=True)
        except OverflowError:
            # probably a livestream
            embed.add_field(name="Duration", value="`Unknown`", inline=True)

        if current_track.album.name:
            embed.add_field(name="Album", value=current_track.album.name, inline=False)
        return embed

    def get_queue(
        self, player: WavelinkPlayer, user: discord.User
    ) -> tuple[discord.Embed, discord.ui.View] | tuple[None, None]:
        current_track = player.current
        if current_track:
            queue = [VoiceMess.current_track_queue(playing_emoji=VoiceMess.playing_emoji, current_track=current_track)]
        else:
            queue = []

        if player.queue:
            future = [track for track in player.queue]
        elif player.autoplay == wavelink.AutoPlayMode.enabled:
            future = [track for track in player.auto_queue]
        else:
            future = []
        for i, track in enumerate(future):
            queue.append(f"{i + 1}. [{track.title}]({track.uri}) - {track.author}")

        if not queue:
            return None, None

        embeds = []
        for i in range(0, len(queue), 10):
            embed = discord.Embed(
                title=f"Queue ({player.queue.count} tracks)", description="\n".join(queue[i : i + 10])
            )
            embeds.append(embed)

        view = PaginationView(user, embeds, show_page=True)
        return embeds, view

    @classmethod
    async def default_checks(cls, inter: discord.Interaction, player: WavelinkPlayer) -> bool:
        """Check if the bot is connected and the user can interact."""
        if not await cls.is_connected(inter, player):
            return False
        if not await cls.can_interact(inter, player):
            return False
        return True

    @classmethod
    async def is_connected(cls, inter: discord.Interaction, player: WavelinkPlayer) -> bool:
        """Check if the bot is connected to a voice channel.

        This should not happen if so update message and return False.
        """
        if not player:
            await inter.message.edit(view=None)
            await inter.response.send_message(VoiceMess.bot_not_connected)
            return False
        return True

    @classmethod
    async def can_interact(cls, inter: discord.Interaction, player: WavelinkPlayer) -> bool:
        """Check if the user can interact with the bot.

        Must be in the voice channel with bot.
        """
        if inter.user not in player.channel.members:
            await inter.response.send_message(VoiceMess.not_in_channel, ephemeral=True)
            return False
        return True

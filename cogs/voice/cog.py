import asyncio
import logging
from typing import cast

import discord
import wavelink
from discord import app_commands
from discord.ext import commands

from cogs.base import Base
from database.voice import PlaylistDB

from .features import Autocomplete, VoiceFeatures, WavelinkPlayer
from .messages import VoiceMess
from .views import VoiceView


@app_commands.guild_only()
class VoiceGroup(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@app_commands.guild_only()
class PlaylistGroup(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Voice(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        Autocomplete.bot = bot

    voice_group = VoiceGroup(name="voice", description=VoiceMess.voice_group_brief)
    playlist_group = PlaylistGroup(name="playlist", description=VoiceMess.playlist_group_brief)

    @voice_group.command(name="play", description=VoiceMess.play_brief)
    @app_commands.autocomplete(query=Autocomplete.autocomp_play)
    async def play(self, inter: discord.Interaction, query: str, place: app_commands.Range[int, 1] = None) -> None:
        """Play a song with the given query."""
        await VoiceFeatures.play(inter, query, place)

    @voice_group.command(name="autoplay", description=VoiceMess.autoplay_brief)
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="Enable", value=wavelink.AutoPlayMode.enabled.value),
            app_commands.Choice(name="Partial", value=wavelink.AutoPlayMode.partial.value),
        ]
    )
    async def autoplay(self, inter: discord.Interaction, mode: app_commands.Choice[int]) -> None:
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        play_mode = {
            wavelink.AutoPlayMode.enabled.value: wavelink.AutoPlayMode.enabled,
            wavelink.AutoPlayMode.partial.value: wavelink.AutoPlayMode.partial,
        }
        player.autoplay = play_mode.get(mode.value)

        if player.autoplay == wavelink.AutoPlayMode.enabled:
            description = VoiceMess.autoplay_on(user=inter.user.mention)
        else:
            description = VoiceMess.autoplay_off(user=inter.user.mention)

        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="skip", description=VoiceMess.skip_brief)
    async def skip(self, inter: discord.Interaction, count: app_commands.Range[int, 1] = None) -> None:
        """Skip the current song."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        if not count:
            await player.skip(force=True)
        else:
            for _ in range(count):
                t = player.queue.get()
                player.queue.history.put(t)
            await player.play(player.queue.get())

        description = VoiceMess.skip(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="move_track", description=VoiceMess.move_brief)
    async def move_track(
        self,
        inter: discord.Interaction,
        old_place: app_commands.Range[int, 1],
        new_place: app_commands.Range[int, 1],
    ) -> None:
        """Move to song from old_place to new_place"""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        track = player.queue.get_at(old_place - 1)

        player.queue.put_at(new_place - 1, track)
        description = VoiceMess.move(user=inter.user.mention, track=track.title, url=track.uri, new_index=new_place)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="filter", description=VoiceMess.filter_brief)
    async def filter(self, inter: discord.Interaction, pitch: int = 1, speed: int = 1, rate: int = 1) -> None:
        """Set the filter to a specific style."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        filters: wavelink.Filters = player.filters
        filters.timescale.set(pitch=pitch, speed=speed, rate=rate)

        await player.set_filters(filters)
        await inter.response.send_message(f"Set filter to pitch: {pitch}, speed: {speed}, rate: {rate}")

    @voice_group.command(name="pause_resume", description=VoiceMess.pause_resume_brief)
    async def pause_resume(self, inter: discord.Interaction) -> None:
        """Pause or Resume the Player depending on its current state."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        embed = await VoiceFeatures.pause_resume(player, inter.user)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="volume", description=VoiceMess.volume_brief)
    async def volume(self, inter: discord.Interaction, value: int) -> None:
        """Change the volume of the player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.set_volume(value)
        description = VoiceMess.volume_set(user=inter.user.mention, volume=value)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="stop", description=VoiceMess.stop_brief)
    async def stop(self, inter: discord.Interaction) -> None:
        """Disconnect the Player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        embed = await VoiceFeatures.stop(player, inter.user)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="shuffle", description=VoiceMess.shuffle_brief)
    async def shuffle(self, inter: discord.Interaction) -> None:
        """Shuffle the queue."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        embed = VoiceFeatures.shuffle_queue(player, inter.user)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="remove", description=VoiceMess.remove_brief)
    async def remove(self, inter: discord.Interaction, place: app_commands.Range[int, 1]) -> None:
        """Remove track from the queue"""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        place = place - 1  # 0 based index
        if place > player.queue.count:
            description = VoiceMess.remove_error(index=place)
            embed = VoiceFeatures.create_embed(description=description)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        track = player.queue.delete(place)
        description = VoiceMess.remove(user=inter.user.mention, track=track, url=track.uri)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="queue", description=VoiceMess.queue_brief)
    async def queue(self, inter: discord.Interaction) -> None:
        """Show the current queue."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await inter.response.send_message(content=VoiceMess.fetching_queue)
        embeds, view = VoiceFeatures.get_queue(player, inter.user)
        if not embeds:
            await inter.edit_original_response(content=VoiceMess.empty_queue)
            return

        await inter.edit_original_response(content="", embed=embeds[0], view=view)
        view.message = await inter.original_response()

    @playlist_group.command(name="play", description=VoiceMess.play_brief)
    @app_commands.autocomplete(name=Autocomplete.autocomp_playlists)
    async def playlist_play(self, inter: discord.Interaction, name: str) -> None:
        """Get playlist from db

        Parameters
        ----------
        name : str
            Guild ID, Author ID, Playlist Name
        """
        guild_id, author_id, playlist_name = name.split(",")
        playlist_url = PlaylistDB.get_playlist(guild_id, author_id, playlist_name)
        if not playlist_url:
            await inter.response.send_message(content=VoiceMess.playlist_not_found(name=playlist_name), ephemeral=True)
            return

        await inter.response.defer()
        await VoiceFeatures.play(inter, playlist_url)

    @playlist_group.command(name="add", description=VoiceMess.add_playlist_brief)
    async def playlist_add(
        self, inter: discord.Interaction, name: app_commands.Range[str, 1, 100], url: str, is_global: bool
    ) -> None:
        """Add playlist to db"""
        await inter.response.defer(ephemeral=True)
        guild_id = str(inter.guild.id) if not is_global else None
        add = PlaylistDB.add_playlist(guild_id, str(inter.user.id), name, url)
        if add is None:
            await inter.edit_original_response(content=VoiceMess.playlist_exists(name=name))
            return

        await inter.edit_original_response(content=VoiceMess.playlist_added(name=add.name, url=add.url))

    @playlist_group.command(name="remove", description=VoiceMess.remove_playlist_brief)
    @app_commands.autocomplete(name=Autocomplete.autocomp_remove_playlists)
    async def playlist_remove(self, inter: discord.Interaction, name: str) -> None:
        """Remove playlist from db

        Parameters
        ----------
        name : str
            Guild ID, Author ID, Playlist Name
        """
        await inter.response.defer(ephemeral=True)
        try:
            guild_id, author_id, playlist_name = name.split(",")
        except ValueError:
            await inter.edit_original_response(content=VoiceMess.use_autocomplete)
            return

        removed = PlaylistDB.remove_playlist(str(inter.user.id), guild_id, author_id, playlist_name)
        if removed is None:
            await inter.edit_original_response(content=VoiceMess.playlist_not_found(name=playlist_name))
            return
        await inter.edit_original_response(content=VoiceMess.playlist_removed(name=removed.name, url=removed.url))

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logging.info(VoiceMess.node_connected(node=f"{payload.node!r}", resumed=payload.resumed))

    @commands.Cog.listener()
    async def on_wavelink_inactive_player(self, player: WavelinkPlayer) -> None:
        description = VoiceMess.inactive(time=player.inactive_timeout)
        embed = VoiceFeatures.create_embed(description=description)

        await player.home.channel.send(embed=embed)
        await player.disconnect()

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: WavelinkPlayer | None = payload.player
        if not player:
            await player.home.channel.send(VoiceMess.bot_not_connected)
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        recommended = original.recommended if original and original.recommended else False

        if hasattr(track.extras, "requester"):
            author = self.bot.get_user(track.extras.requester)
        else:
            author = self.bot.user
        embed = VoiceFeatures.now_playing_embed(player, author, recommended=recommended)

        if not hasattr(player, "view"):
            player.view = VoiceView(self.bot)

        message = await player.home.channel.send(embed=embed, view=player.view)
        player.message = message

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload) -> None:
        player: WavelinkPlayer | None = payload.player
        if player:
            await player.message.edit(view=None)
            return

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self, payload: wavelink.TrackStuckEventPayload) -> None:
        player: WavelinkPlayer | None = payload.player
        if not player:
            await player.home.channel.send(VoiceMess.bot_not_connected)
            return

        await player.skip(force=True)
        embed = VoiceFeatures.create_embed(description=VoiceMess.stuck)
        await player.message.edit(view=None)
        await player.message.reply(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel_id = before.channel.id if before.channel else after.channel.id
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        # check users in channel
        members = channel.members
        users = [member for member in members if not member.bot]
        if users:
            return

        player: WavelinkPlayer = cast(WavelinkPlayer, channel.guild.voice_client)
        if not player:
            # bot not connected
            return

        # wait again if users join
        await asyncio.sleep(player.inactive_timeout)

        # check users in channel
        members = channel.members
        users = [member for member in members if not member.bot]
        if users:
            return

        if not player:
            # bot not connected
            return

        # disconnect the player
        await player.message.edit(view=None)
        description = VoiceMess.inactive(time=player.inactive_timeout)
        embed = VoiceFeatures.create_embed(description=description)
        await player.home.channel.send(embed=embed)
        await player.disconnect()

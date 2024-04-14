import asyncio
import logging
from typing import cast

import discord
import wavelink
from discord import app_commands
from discord.ext import commands

from cogs.base import Base
from database.voice import PlaylistDB

from .features import VoiceFeatures, WavelinkPlayer
from .messages import VoiceMess
from .views import VoiceView

playlists = {}


async def autocomp_playlists(inter: discord.Interaction, user_input: str):
    guild_playlists = playlists[inter.guild.id]
    return [
        app_commands.Choice(name=playlist.name, value=playlist.link)
        for playlist in guild_playlists
        if user_input.lower() in playlist
    ]


@app_commands.guild_only()
class VoiceGroup(app_commands.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Voice(Base, commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        global playlists
        # playlists = self.get_playlists()

    def get_playlists(self):
        guilds = PlaylistDB.get_guilds()
        for guild in guilds:
            playlists[guild] = PlaylistDB.get_playlists(guild)

    voice_group = VoiceGroup(name="voice", description=VoiceMess.voice_group_brief)

    @voice_group.command(name="play", description=VoiceMess.play_brief)
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

        await player.pause(not player.paused)
        if player.paused:
            description = VoiceMess.pause(user=inter.user.mention)
        else:
            description = VoiceMess.resume(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
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

        await player.disconnect()
        description = VoiceMess.stop(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @voice_group.command(name="shuffle", description=VoiceMess.shuffle_brief)
    async def shuffle(self, inter: discord.Interaction) -> None:
        """Shuffle the queue."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        if player.autoplay == wavelink.AutoPlayMode.enabled:
            player.auto_queue.shuffle()
        else:
            player.queue.shuffle()
        description = VoiceMess.shuffle(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
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

        track = player.queue.peek(place)
        player.queue.remove(place)
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
        embeds, view = VoiceFeatures.get_queue(inter, player, inter.user)
        if not embeds:
            await inter.edit_original_response(content=VoiceMess.empty_queue)
            return

        await inter.edit_original_response(content="", embed=embeds[0], view=view)
        view.message = await inter.original_response()

    # @voice_group.command(name="playlist", description=VoiceMess.play_brief)
    # @app_commands.autocomplete(name=autocomp_playlists)
    # async def playlist(self, inter: discord.Interaction, name: str) -> None:
    #     """Get playlist from db"""
    #     playlist = PlaylistDB.get_playlist(inter.guild.id, name)
    #     await VoiceFeatures.play(inter, playlist.url)

    @voice_group.command(name="add_playlist", description=VoiceMess.add_playlist_brief)
    async def add_playlist(self, inter: discord.Interaction, name: str, url: str) -> None:
        """Add playlist to db"""
        await inter.response.defer(ephemeral=True)
        add = PlaylistDB.add_playlist(inter.guild.id, name, url)
        if add is None:
            await inter.edit_original_response(content=f"Playlist with name {name} already exists\n")
            return
        await inter.edit_original_response(content=f"Playlist {name} added\n{url}")

    @voice_group.command(name="remove_playlist", description=VoiceMess.remove_playlist_brief)
    async def remove_playlist(self, inter: discord.Interaction, name: str, url: str) -> None:
        """Remove playlist from db"""
        await inter.response.defer(ephemeral=True)
        remove = PlaylistDB.remove_playlist(inter.guild.id, inter.user.id, name)
        if remove is None:
            await inter.edit_original_response(content=f"Playlist with name {name} doesn't exists\n")
            return
        await inter.edit_original_response(content=f"Playlist {name} removed\n{url}")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logging.info(f"Wavelink Node connected: {payload.node!r} | Resumed: {payload.resumed}")

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

        # disconnect the player
        await player.message.edit(view=None)
        description = VoiceMess.inactive(time=player.inactive_timeout)
        embed = VoiceFeatures.create_embed(description=description)
        await player.home.channel.send(embed=embed)
        await player.disconnect()

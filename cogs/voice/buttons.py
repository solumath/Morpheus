from typing import cast

import discord
import wavelink
from discord.ext import commands

from .features import VoiceFeatures, WavelinkPlayer
from .messages import VoiceMess


# TODO guild config in db?
class VoiceView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Down", emoji="🔉", style=discord.ButtonStyle.secondary, custom_id="voice:volume_down")
    async def volume_down_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Change the volume of the player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.set_volume(player.volume - 10)
        description = VoiceMess.volume_down(user=inter.user.mention, volume=player.volume)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Back", emoji="⏮️", style=discord.ButtonStyle.secondary, custom_id="voice:back")
    async def back_button(self, inter: discord.Interaction, button: discord.ui.Button):
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.pause(not player.paused)

        description = VoiceMess.back(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.message.edit(view=self)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Pause", emoji="⏸️", style=discord.ButtonStyle.secondary, custom_id="voice:pause")
    async def pause_resume_button(self, inter: discord.Interaction, button: discord.ui.Button):
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.pause(not player.paused)
        if player.paused:
            description = VoiceMess.pause(user=inter.user.mention)
        else:
            description = VoiceMess.resume(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)

        button.emoji = "▶️" if player.paused else "⏸️"
        button.label = "Resume" if player.paused else "Pause"

        await inter.message.edit(view=self)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Skip", emoji="⏭️", style=discord.ButtonStyle.secondary, custom_id="voice:next")
    async def next_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Skip the current song."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.skip(force=True)
        description = VoiceMess.skip(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Up", emoji="🔊", style=discord.ButtonStyle.secondary, custom_id="voice:volume_up")
    async def volume_up_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Change the volume of the player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.set_volume(player.volume + 10)
        description = VoiceMess.volume_up(user=inter.user.mention, volume=player.volume)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Shuffle", emoji="🔀", style=discord.ButtonStyle.secondary, custom_id="voice:shuffle")
    async def shuffle_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Randomize the queue."""
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

    @discord.ui.button(label="Looping off", emoji="⛔", style=discord.ButtonStyle.secondary, custom_id="voice:loop")
    async def loop_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Change the volume of the player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        if player.queue.mode == wavelink.QueueMode.normal:
            player.queue.mode = wavelink.QueueMode.loop_all
            button.label = "Looping queue"
            button.emoji = "🔁"
            description = VoiceMess.loop_queue(user=inter.user.mention)
        elif player.queue.mode == wavelink.QueueMode.loop_all:
            player.queue.mode = wavelink.QueueMode.loop
            button.label = "Looping track"
            button.emoji = "🔂"
            description = VoiceMess.loop_track(user=inter.user.mention)
        else:
            player.queue.mode = wavelink.QueueMode.normal
            button.label = "Looping off"
            button.emoji = "⛔"
            description = VoiceMess.loop_off(user=inter.user.mention)

        embed = VoiceFeatures.create_embed(description=description)
        await inter.message.edit(view=self)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Stop", emoji="⏹️", style=discord.ButtonStyle.secondary, custom_id="voice:stop")
    async def stop_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Change the volume of the player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        await player.disconnect()
        description = VoiceMess.stop(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.message.edit(view=None)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Autoplay", emoji="⛔", style=discord.ButtonStyle.secondary, custom_id="voice:autoplay")
    async def autoplay_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Change the autoplay mode."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        if player.autoplay == wavelink.AutoPlayMode.partial:
            player.autoplay = wavelink.AutoPlayMode.enabled
            button.emoji = "✅"
            description = VoiceMess.autoplay_on(user=inter.user.mention)
        else:
            player.autoplay = wavelink.AutoPlayMode.partial
            button.emoji = "⛔"
            description = VoiceMess.autoplay_off(user=inter.user.mention)

        embed = VoiceFeatures.create_embed(description=description)
        await inter.message.edit(view=self)
        await inter.response.send_message(embed=embed)

    @discord.ui.button(label="Clear", emoji="🗑️", style=discord.ButtonStyle.secondary, custom_id="voice:clear")
    async def clear_button(self, inter: discord.Interaction, button: discord.ui.Button):
        """Change the volume of the player."""
        player: WavelinkPlayer = cast(WavelinkPlayer, inter.guild.voice_client)
        if not await VoiceFeatures.default_checks(inter, player):
            return

        if player.autoplay == wavelink.AutoPlayMode.enabled:
            player.auto_queue.reset()
        else:
            player.queue.reset()
        description = VoiceMess.clear(user=inter.user.mention)
        embed = VoiceFeatures.create_embed(description=description)
        await inter.response.send_message(embed=embed)

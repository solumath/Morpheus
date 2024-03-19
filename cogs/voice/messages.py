from config.messages import GlobalMessages


class VoiceMess(GlobalMessages):
    voice_group_brief = "Voice commands"
    play_brief = "Play a song with the given query (can be url)"
    skip_brief = "Skip the current song"
    nightcore_brief = "Set the filter to a nightcore style"
    filter_brief = "Set the filter to a specific style. Default is normal"
    pause_resume_brief = "Pause or Resume the Player depending on its current state"
    autoplay_brief = "Toggle autoplay"
    add_playlist_brief = "Add a playlist to the database"
    remove_playlist_brief = "Remove a playlist from database"
    bot_not_connected = "Bot is not connected to voice"
    unable_to_join = "I was unable to join this voice channel. Please try again."
    join_channel = "Please join a voice channel first before using this command."
    home_channel = "You can only play songs in {channel}, as the player has already started there."
    pause = "⏸️ {user} Paused the player"
    resume = "▶️ {user} Resumed the player"
    stop = "⏹️ {user} Destroyed the player"
    skip = "⏭️ {user} Skipped the song"
    back = "⏮️ {user} Went back to the previous song"
    volume_up = "🔊 {user} Increased the volume to {volume}"
    volume_down = "🔉 {user} Decreased the volume to {volume}"
    volume_set = "🔊 {user} Set the volume to {volume}"
    shuffle = "🔀 {user} Shuffled the queue"
    autoplay_on = "✅ {user} Turned on autoplay"
    autoplay_off = "⛔ {user} Turned off autoplay"
    clear = "🗑️ {user} Cleared the queue"
    loop_off = "⛔ {user} Toggled the loop off"
    loop_queue = "🔁 {user} Toggled the loop all"
    loop_track = "🔂 {user} Toggled the loop track"
    remove = "🗑️ {user} Removed [{track}]({url}) from the queue"
    remove_error = "There is no track at {index} place"
    move = "↔️ {user} Moved [{track}]({url}) to place {new_index}"
    playing_emoji = "<a:playing:1207081978264817734>"
    current_track = "{playing_emoji} [`{current_track.title}`]({current_track.uri})"
    current_track_queue = "{playing_emoji} [`{current_track.title}`]({current_track.uri}) - {current_track.author} {playing_emoji}"
    inactive = "The player has been idle for `{time}` seconds. Goodbye!"
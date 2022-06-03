import disnake
from disnake.ext import commands
from disnake import TextChannel, Embed
from config import messages, channels
import utility
import os
import traceback
import git
import keys

messages = messages.Messages
channels = channels.Channels

bot = commands.Bot(command_prefix="?", intents=disnake.Intents.all(), test_guilds=channels.guild_ids)

@bot.event
async def on_ready():
    print(messages.on_ready_bot.format(bot.user, bot.user.id))

    #set status for bot
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    await bot.change_presence(activity=disnake.Game(f"/help | On commit {sha[:7]}"))
    bot_room: TextChannel = bot.get_channel(channels.development)
    if bot_room is not None:
        await bot_room.send(messages.on_ready_bot.format(bot.user.mention, bot.user.id))

@bot.slash_command(name="purge", description="delete number of messages")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number_of_messages : int):
    await ctx.channel.purge(limit=number_of_messages)
    await ctx.send("What is real? How do you define real?", delete_after=5)

#-------------------------Cogs----------------------------
async def all_loaded_cogs():
    cogs = bot.cogs
    cog_names = []
    for cog in cogs:
        cog_names.append(f"{cog.lower()}")
    return cog_names

async def cogs_loaded(inter: disnake.CommandInteraction, user_input: str):
    cogs = await all_loaded_cogs()
    return [cog for cog in cogs if user_input.lower() in cog]

async def cogs_not_loaded(inter: disnake.CommandInteraction, user_input: str):
    all_cogs = []
    for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                all_cogs.append(filename[:-3])

    loaded = await all_loaded_cogs()
    cogs = list(set(loaded)^set(all_cogs))
    if cogs:
        return [cog for cog in cogs if user_input.lower() in cog]
    else:
        return ["All cogs loaded."]

async def loading(msg, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        msg.append(messages.succes_load.format(extension))
    except commands.ExtensionFailed:
        msg.append(messages.fail_load.format(extension))
    except commands.ExtensionNotFound:
        msg.append(messages.not_found.format(extension))
    except commands.ExtensionAlreadyLoaded:
        msg.append(messages.already_loaded.format(extension))

async def unloading(msg, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        msg.append(messages.succes_unload.format(extension))
    except commands.ExtensionNotFound:
        msg.append(messages.not_found.format(extension))
    except commands.ExtensionNotLoaded:
        msg.append(messages.not_loaded.format(extension))

async def reloading(msg, extension):
    try:
        bot.reload_extension(f"cogs.{extension}")  
        msg.append(messages.succes_reload.format(extension))
    except commands.ExtensionFailed:
        msg.append(messages.fail_reload.format(extension))
    except commands.ExtensionNotFound:
        msg.append(messages.not_found.format(extension))
    except commands.ExtensionNotLoaded:
        msg.append(messages.not_loaded.format(extension))

# slash commands for manipulating with extensions
@bot.slash_command(name="load", description="Loads cog(s) file")
@commands.has_permissions(administrator=True)
async def load(ctx, all: bool = False, extension: str = commands.Param(autocomplete=cogs_not_loaded)):
    msg = []
    if all:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await loading(msg, filename[:-3])
    else:
        await loading(msg, extension)

    print(*msg, sep = "\n")
    await ctx.send("\n".join(msg))

@bot.slash_command(name="unload", description="Unloads cog(s) file")
@commands.has_permissions(administrator=True)
async def unload(ctx, all: bool = False, extension: str = commands.Param(autocomplete=cogs_loaded)):
    msg = []
    if all:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await unloading(msg, filename[:-3])
    else:
        await unloading(msg, extension)

    print(*msg, sep = "\n")
    await ctx.send("\n".join(msg))

@bot.slash_command(name="reload", description="Reloads cog(s) file")
@commands.has_permissions(administrator=True)
async def rel(ctx, all: bool = False, extension: str = commands.Param(autocomplete=cogs_loaded)):
    msg = []
    if all:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await reloading(msg, filename[:-3])
    else:
        await reloading(msg, extension)

    print(*msg, sep = "\n")
    await ctx.send("\n".join(msg))

@bot.slash_command(name="cogs", description="List of loaded cogs")
@commands.has_permissions(administrator=True)
async def cogs(ctx):
    cogs = bot.cogs
    cog_names = []
    for cog in cogs:
        cog_names.append(str(cog))
    await ctx.send("\n".join(cog_names))

#load all cogs and remove extension from name
for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_error(event, *args, **kwargs):
    channel_out = bot.get_channel(channels.development)
    output = traceback.format_exc()
    print(output)

    embeds = []
    guild = None
    for arg in args:
        if arg.guild_id:
            guild = bot.get_guild(arg.guild_id)
            event_guild = guild.name
            channel = guild.get_channel(arg.channel_id)
            message = await channel.fetch_message(arg.message_id)
            message = message.content[:1000]
        else:
            event_guild = "DM"
            message = arg.message_id

        user = bot.get_user(arg.user_id)
        if not user:
            user = arg.user_id
        else:
            channel = bot.get_channel(arg.channel_id)
            if channel:
                message = await channel.fetch_message(arg.message_id)
                if message.content:
                    message = message.content[:1000]
                elif message.embeds:
                    embeds.extend(message.embeds)
                    message = "Embed v předchozí zprávě"
                elif message.attachments:
                    message_out = ""
                    for attachment in message.attachments:
                        message_out += f"{attachment.url}\n"
                    message = message_out
            else:
                message = arg.message_id
            user = str(user)
        embed = Embed(title=f"Ignoring exception on event '{event}'", color=0xFF0000)
        embed.add_field(name="Zpráva", value=message, inline=False)
        if arg.guild_id != channels.my_guild:
            embed.add_field(name="Guild", value=event_guild)

    if channel_out is not None:
        output = utility.cut_string(output, 1900)
        for embed in embeds:
            await channel_out.send(embed=embed)
        for message in output:
            await channel_out.send(f"```\n{message}```")

bot.run(keys.TOKEN)

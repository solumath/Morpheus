from genericpath import isdir, isfile
import disnake
from disnake.ext import commands
from disnake import TextChannel, Embed
from config.messages import Messages
from config.channels import Channels
import utility
import os
import traceback
import git
import keys

bot = commands.Bot(command_prefix="?", intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(Messages.on_ready_bot.format(bot.user, bot.user.id))

    #set status for bot
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    await bot.change_presence(activity=disnake.Game(f"/help | On commit {sha[:7]}"))
    bot_room: TextChannel = bot.get_channel(Channels.development)
    if bot_room is not None:
        await bot_room.send(Messages.on_ready_bot.format(bot.user.mention, bot.user.id))

@commands.has_permissions(manage_messages=True)
@bot.slash_command(name="purge", description="delete number of messages")
async def purge(ctx, number_of_messages : int):
    await ctx.channel.purge(limit=number_of_messages)
    await ctx.send("What is real? How do you define real?", delete_after=5)


#load all cogs and remove extension from name
for name in os.listdir("./cogs"):
    filename = f"./cogs/{name}"
    modulename = f"cogs.{name}"

    if isfile(filename) and filename.endswith(".py"):
        bot.load_extension(modulename[:-3])
    
    if isdir(filename) and ("__init__.py" in os.listdir(filename)):
        bot.load_extension(modulename)


@bot.event
async def on_error(event, *args, **kwargs):
    channel_out = bot.get_channel(Channels.development)
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
        if arg.guild_id != Channels.my_guild:
            embed.add_field(name="Guild", value=event_guild)

    if channel_out is not None:
        output = utility.cut_string(output, 1900)
        for embed in embeds:
            await channel_out.send(embed=embed)
        for message in output:
            await channel_out.send(f"```\n{message}```")


bot.run(keys.TOKEN)

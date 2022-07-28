import disnake
from disnake.ext import commands
from disnake import TextChannel
from config.messages import Messages
from config.channels import Channels
from genericpath import isdir, isfile
import os
import git
import keys

bot = commands.Bot(command_prefix="?", intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(Messages.on_ready_bot.format(bot.user, bot.user.id))

    # set status for bot
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    await bot.change_presence(activity=disnake.Game(f"/help | On commit {sha[:7]}"))
    bot_room: TextChannel = bot.get_channel(Channels.development)
    if bot_room is not None:
        await bot_room.send(Messages.on_ready_bot.format(bot.user.mention, bot.user.id))

# load all cogs and remove extension from name
for name in os.listdir("./cogs"):
    filename = f"./cogs/{name}"
    modulename = f"cogs.{name}"

    if isfile(filename) and filename.endswith(".py"):
        bot.load_extension(modulename[:-3])

    if isdir(filename) and ("__init__.py" in os.listdir(filename)):
        bot.load_extension(modulename)


bot.run(keys.TOKEN)

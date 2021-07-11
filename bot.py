import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

import os
import json
import traceback
import git

import env

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=None)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload = True)

@bot.event
async def on_ready():
    print('Ready!')
    print('Logged in as', bot.user)
    print('ID:', bot.user.id)

    #set status for bot
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    await bot.change_presence(activity=discord.Game(f"/help | On commit {sha[:7]}"))

@slash.slash(name="purge", description="delete number of messages")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number_of_messages : int):
    await ctx.channel.purge(limit=number_of_messages)
    await ctx.send("What is real? How do you define real?", delete_after=5)

#-------------------------Cogs----------------------------
@slash.slash(name="load", description="Loads cog(s) file")
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    msg = []
    cogs = list(extension.split(" "))
    for cog in cogs:
        try:
            bot.load_extension(f"cogs.{cog}")
            msg.append(f"Loaded successfully **{cog}**")
        except commands.ExtensionFailed:
            msg.append(f"Failed to load **{cog}**")
        except commands.ExtensionNotFound:
            msg.append(f"Not found **{cog}**")
        except commands.ExtensionAlreadyLoaded:
            msg.append(f"Already loaded **{cog}**")
    print(*msg, sep = "\n")
    await ctx.send("\n".join(msg))

@slash.slash(name="unload", description="Unloads cog(s) file")
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    msg = []
    cogs = list(extension.split(" "))
    for cog in cogs:
        try:
            bot.unload_extension(f"cogs.{cog}")
            msg.append(f"Unloaded successfully **{cog}**")
        except commands.ExtensionNotFound:
            msg.append(f"Not found **{cog}**")
        except commands.ExtensionNotLoaded:
            msg.append(f"Not loaded **{cog}**")
    print(*msg, sep = "\n")
    await ctx.send("\n".join(msg))

@slash.slash(name="reload", description="Reloads cog(s) file")
@commands.has_permissions(administrator=True)
async def rel(ctx, extension):
    msg = []
    cogs = list(extension.split(" "))
    for cog in cogs:
        try:
            bot.reload_extension(f"cogs.{cog}")  
            msg.append(f"Reloaded successfully **{cog}**")
        except commands.ExtensionFailed:
            msg.append(f"Failed to reload **{cog}**")
        except commands.ExtensionNotFound:
            msg.append(f"Not found **{cog}**")
        except commands.ExtensionNotLoaded:
            msg.append(f"Not loaded **{cog}**")
    print(*msg, sep = "\n")
    await ctx.send("\n".join(msg))

@slash.slash(name="reloadall", description="Reloads all cog files")
@commands.has_permissions(administrator=True)
async def reloadall(ctx):
    cogs = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.reload_extension(f"cogs.{filename[:-3]}")
                cogs.append(f"Reloaded successfully **{filename[:-3]}**")
            except commands.ExtensionFailed:
                cogs.append(f"Failed to reload **{filename[:-3]}**")
            except commands.ExtensionNotFound:
                cogs.append(f"Not found **{filename[:-3]}**")
            except commands.ExtensionNotLoaded:
                cogs.append(f"Not loaded **{filename[:-3]}**")
    print(*cogs, sep = "\n")
    await ctx.send("\n".join(cogs))

@slash.slash(name="cogs", description="List of loaded cogs")
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
    if event == "on_slash_command_error":
        pass

    else:
        channel = bot.get_channel(env.development)
        ex = traceback.format_exc()

        embed = discord.Embed(title="Ignoring exception", colour=0xFF0000)
        embed.add_field(name="Traceback", value=f"```{ex}```")

        print(ex)
        await channel.send(embed=embed)

bot.run(env.TOKEN)
import discord
from discord.ext import commands
import os
import json
import env
from discord_slash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload = True)

@slash.slash(name="purge", description="delete number of messages")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number_of_messages : int):
    await ctx.channel.purge(limit=number_of_messages)
    await ctx.send("What is real? How do you define real?", delete_after=5)

#-------------------------Cogs----------------------------
@slash.slash(name="load", description="Loads cog file")
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    try:
        bot.load_extension(f'cogs.{extension}')
        print(f'Loading cog {extension} successful')
        await ctx.send(f'Loading {extension} successful')
    except commands.ExtensionFailed:
        await ctx.send("Cog failed to load")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is already loaded")
    

@slash.slash(name="unload", description="Unloads cog file")
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        print(f'Unloading cog {extension} successful')
        await ctx.send(f'Unloading {extension} successful')
    except commands.ExtensionFailed:
        await ctx.send("Cog failed to unload")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    except commands.ExtensionNotLoaded:
        await ctx.send("Cog is not loaded")

@slash.slash(name="reload", description="Reloads cog file")
@commands.has_permissions(administrator=True)
async def rel(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')  
        bot.load_extension(f'cogs.{extension}')
        print(f'Reloading cog {extension} successful')
        await ctx.send(f'Reloading {extension} successful')
    except commands.ExtensionFailed:
        await ctx.send("Cog failed to reload")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    except commands.ExtensionNotLoaded:
        await ctx.send("Cog is not loaded")

@slash.slash(name="reloadall", description="Reloads all cog files")
@commands.has_permissions(administrator=True)
async def reloadall(ctx):
    cogs = []
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cogs.append(f'Loaded cog {filename[:-3]}')
            except:
                cogs.append(f'Unable to load {filename[:-3]}')

    print(*cogs, sep = "\n")
    await ctx.send('\n'.join(cogs))


#load all cogs and remove extension from name
for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(env.TOKEN)
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
    print(f'Loading cog {extension}')
    await ctx.send(f'Loading {extension}')
    try:
        bot.load_extension(f'cogs.{extension}')
        print(f'Loading cog {extension} successful')
        await ctx.send(f'Loading {extension} successful')
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is already loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    except commands.ExtensionFailed:
        await ctx.send("Cog failed to load")

@slash.slash(name="unload", description="Unloads cog file")
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    print(f'Unloading cog {extension}')
    await ctx.send(f'Unloading {extension}')
    try:
        bot.unload_extension(f'cogs.{extension}')
        print(f'Unloading cog {extension} successful')
        await ctx.send(f'Unloading {extension} successful')
    except commands.ExtensionNotLoaded:
        await ctx.send("Cog is not loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    except commands.ExtensionFailed:
        await ctx.send("Cog failed to unload")

@slash.slash(name="reload", description="Reloads cog file")
@commands.has_permissions(administrator=True)
async def rel(ctx, extension):
    print(f'Reloading cog {extension}')
    await ctx.send(f'Reloading {extension}')
    
    bot.unload_extension(f'cogs.{extension}')  
    bot.load_extension(f'cogs.{extension}') 

    print(f'Reloading cog {extension} successful')
    await ctx.send(f'Reloading {extension} successful')

@slash.slash(name="reloadall", description="Reloads all cog files")
@commands.has_permissions(administrator=True)
async def reloadall(ctx):
    """Reloads all cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded cog {filename[:-3]}')
            await ctx.send(f'Loaded cog {filename[:-3]}')
        else:
            print(f'Unable to load {filename[:-3]}')
            await ctx.send(f'Unable to load cog {filename[:-3]}')

for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


#-------------------------Errors----------------------------
@bot.event
async def on_slash_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I do not posses that command")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You cannot beat me!")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Your argument is invalid")

    else:
        raise error
        await ctx.send(error)

bot.run(env.TOKEN)
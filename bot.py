import discord
from discord.ext import commands
import os
import json
import env

intents = discord.Intents.all()

description = '''Kaneki Tryhardbot'''
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.command(name="clear", aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, numberOfMessages : int):
    """delete X messages"""
    await ctx.message.channel.purge(limit=numberOfMessages)

#-------------------------Cogs----------------------------

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    """Loads cog file"""
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

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    """Unloads cog file"""
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

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    """Unload + load cog file"""
    print(f'Reloading cog {extension}')
    await ctx.send(f'Reloading {extension}')
    
    bot.unload_extension(f'cogs.{extension}')  
    bot.load_extension(f'cogs.{extension}') 

    print(f'Reloading cog {extension} successful')
    await ctx.send(f'Reloading {extension} successful')

@bot.command()
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
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Takový příkaz neumím")

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Na tento příkaz nemáš práva")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Chybí ti argument")

    else:
        raise error


bot.run(env.TOKEN)

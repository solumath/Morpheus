import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import os
import json
import init

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
    print('Loading cog {}'.format(extension))
    await ctx.send('Loading {}'.format(extension))
    try:
        bot.load_extension(f'cogs.{extension}')
        print('Loading cog {} successful'.format(extension))
        await ctx.send('Loading {} successful'.format(extension))
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
    print('Unloading cog {}'.format(extension))
    await ctx.send('Unloading {}'.format(extension))
    try:
        bot.unload_extension(f'cogs.{extension}')
        print('Unloading cog {} successful'.format(extension))
        await ctx.send('Unloading {} successful'.format(extension))
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
    print('Reloading cog {}'.format(extension))
    await ctx.send('Reloading {}'.format(extension))
    
    bot.unload_extension(f'cogs.{extension}')  
    bot.load_extension(f'cogs.{extension}') 
    
    print('Reloading cog {} successful'.format(extension))
    await ctx.send('Reloading {} successful'.format(extension))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#-------------------------Errors----------------------------
@load.error
@unload.error
@reload.error
@clear.error
async def clear_error(error, ctx):
    if isinstance(error, MissingPermissions):
       await ctx.send("You don't have permission to do that...")

bot.run(init.TOKEN)
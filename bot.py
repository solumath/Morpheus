import discord
from discord.ext import commands

import os
import json
import init

description = '''Kaneki Tryhardbot'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")

@bot.command()
async def clear(ctx, numberOfMessages : int):
    """delete X messages"""
    await ctx.message.channel.purge(limit=numberOfMessages)

#-------------------------Cogs----------------------------

@bot.command()
async def load(ctx, extension):
    """Loads cog file"""
    bot.load_extension(f'cogs.{extension}')
    print('Load cog {}'.format(extension))

@bot.command()
async def unload(ctx, extension):
    """Unloads cog file"""
    bot.unload_extension(f'cogs.{extension}')
    print('Unload cog {}'.format(extension))

@bot.command()
async def reload(ctx, extension):
    """Unload + load"""
    bot.unload_extension(f'cogs.{extension}')  
    bot.load_extension(f'cogs.{extension}') 
    print('Reload cog {}'.format(extension))
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(init.TOKEN)

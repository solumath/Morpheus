import discord
from init import TOKEN
import json
from discord.ext import commands

description = '''Kaneki Tryhardbot'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")


@bot.command()
async def add(ctx, left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def clear(ctx, numberOfMessages : int):
    await ctx.message.channel.purge(limit=numberOfMessages)

@bot.command()
async def diff(ctx, left : int, right : int):
    """Difference two numbers together."""
    await ctx.send(left - right)

@bot.command()
async def sum(ctx, left : int, right : int):
    """Sum two numbers together."""
    await ctx.send(left * right)

@bot.command()
async def div(ctx, left : int, right : int):
    """Divide two numbers together."""
    await ctx.send(left / right)

bot.run(TOKEN)

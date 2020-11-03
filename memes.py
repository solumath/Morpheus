

@bot.event
async def on_message(message):
    if message.author.bot:
        if message.author.id == bot.user.id and \
            message.content.startswith("<:") and \
            message.content.endswith(">"):
             await message.channel.send(message.content)
        return
    elif "uh oh" in message.content:
        await message.channel.send("uh oh")
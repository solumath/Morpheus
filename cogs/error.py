import disnake
from disnake.ext import commands

import traceback
import utility
from config.messages import Messages
from config.channels import Channels

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.response.send_message(Messages.not_enough_perms)
            return
        if isinstance(error, commands.CommandOnCooldown):
            await inter.response.send_message(Messages.command_cooldowns.format(time = round(error.retry_after, 1)))
            return
        if isinstance(error, disnake.InteractionTimedOut):
            await inter.response.send_message(Messages.command_timed_out)
            return

        channel = self.bot.get_channel(Channels.development)
        await inter.response.send_message(f"```Errors happen Mr. Anderson```")
        url = f"https://discord.com/channels/{inter.guild_id}/{inter.channel_id}/{inter.id}"

        output = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        embed = disnake.Embed(title=f"Ignoring exception on command {inter.data.name}", color=0xFF0000)
        embed.add_field(name="Autor", value=str(inter.author))

        if inter.guild and inter.guild.id != Channels.my_guild:
            embed.add_field(name="Guild", value=inter.guild.name)
        embed.add_field(name="Zpráva", value=inter.filled_options, inline=False)
        embed.add_field(name="Link", value=url, inline=False)

        print(output)
        await channel.send(embed=embed)

        output = utility.cut_string(output, 1900)
        if channel is not None:
            for message in output:
                await channel.send(f"```\n{message}\n```")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(Messages.not_enough_perms)
            return
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(error)
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(Messages.command_cooldowns.format(time = round(error.retry_after, 1)))
            return
        if isinstance(error, commands.UserInputError):
            await ctx.send(error)
            return

        channel = self.bot.get_channel(Channels.development)
        message = await ctx.send(f"```Errors happen Mr. Anderson```")

        output = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        embed = disnake.Embed(title=f"Ignoring exception on command {ctx.command}", color=0xFF0000)
        embed.add_field(name="Autor", value=str(ctx.author))

        if ctx.guild and ctx.guild.id != Channels.my_guild:
            embed.add_field(name="Guild", value=ctx.guild.name)
        embed.add_field(name="Zpráva", value=ctx.message.content[:1000], inline=False)
        embed.add_field(name="Link", value=ctx.message.jump_url, inline=False)

        print(output)
        await channel.send(embed=embed)

        output = utility.cut_string(output, 1900)
        if channel is not None:
            for message in output:
                await channel.send(f"```\n{message}\n```")


def setup(bot):
    bot.add_cog(Error(bot))

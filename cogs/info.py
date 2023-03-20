import json
from datetime import datetime

import disnake
import requests
from disnake.ext import commands

from config.messages import Messages


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open(f"servers/{member.guild.name}/config.json", 'r') as f:
            info_channel = json.load(f)
        channel = self.bot.get_channel(int(info_channel["joined"]))
        await channel.send(Messages.welcome.format(member.mention))

    @commands.slash_command(name="kredity", description="Prints out credits for BIT")
    async def kredity(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(Messages.kredity)

    @commands.slash_command(name="user", description="Prints out info about user")
    async def user_info(self, inter: disnake.ApplicationCommandInteraction, target: disnake.Member = None):
        target = target or inter.author

        headers = {
                    'authorization': ''
                    }
        r = requests.get(f'https://discord.com/api/v9/guilds/{inter.guild.id}/messages/search?author_id={target.id}&include_nsfw=true', headers=headers)  # noqa: E501
        data = json.loads(r.text)

        embed = disnake.Embed(
                        title="User information",
                        color=target.color,
                        timestamp=datetime.utcnow())

        if target.avatar is not None:
            embed.set_thumbnail(url=target.avatar)

        fields = [("Name", str(target), True),
                  ("ID", target.id, True),
                  ("Status", str(target.status).title(), False),
                  ("Role", ' '.join([role.mention for role in target.roles[1:][::-1]]), False),
                  ("Created account", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined server", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Total messages", data['total_results'], False),
                  ("Boosted", bool(target.premium_since), False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="server", description="Prints out info about server")
    async def server_info(self, inter: disnake.ApplicationCommandInteraction):
        embed = disnake.Embed(
                                title="Server information",
                                colour=inter.guild.owner.colour,
                                timestamp=datetime.utcnow()
                                )

        if inter.guild.icon is not None:
            embed.set_thumbnail(url=inter.guild.icon)

        statuses = [
                    len(list(filter(lambda m: str(m.status) == "online", inter.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", inter.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", inter.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", inter.guild.members)))]

        fields = [
                ("ID", inter.guild.id, True),
                ("Owner", inter.guild.owner.mention, True),
                ("Created at", inter.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Members", len(inter.guild.members), True),
                ("Humans", len(list(filter(lambda m: not m.bot, inter.guild.members))), True),
                ("Bots", len(list(filter(lambda m: m.bot, inter.guild.members))), True),
                ("Banned members", len(await inter.guild.bans().flatten()), True),
                ("Statuses", f"🟩 {statuses[0]} 🟧 {statuses[1]} 🟥 {statuses[2]} ⬛ {statuses[3]}", True),
                ("Text channels", len(inter.guild.text_channels), True),
                ("Voice channels", len(inter.guild.voice_channels), True),
                ("Categories", len(inter.guild.categories), True),
                ("Roles", len(inter.guild.roles), True),
                ("Invites", len(await inter.guild.invites()), True),
                ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))

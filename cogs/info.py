import discord
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class Info(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="info", aliases=["memberinfo", "me", "userinfo"])
	async def user_info(self, ctx, target: discord.Member = None):
		"""prints out info about user"""
		target = target or ctx.author

		embed = Embed(title="User information",
					  color=target.color,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=target.avatar_url)

		fields = [("Name", str(target), True),
				  ("ID", target.id, True),
				  ("Status", str(target.status), True),
				  ("Role", ["{}".format(tg.name) for tg in target.roles[1:]], False),
				  ("Created account", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Joined server", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Boosted", bool(target.premium_since), True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

	@command(name="server", aliases=["serverinfo", "guildinfo"])
	async def server_info(self, ctx):
		"""prints out info about server"""
		embed = Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=ctx.guild.icon_url)

		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Statuses", f"🟩 {statuses[0]} 🟧 {statuses[1]} 🟥 {statuses[2]} ⬛ {statuses[3]}", True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Info(bot))
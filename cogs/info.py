import disnake
from disnake.ext import commands
from datetime import datetime
import json
import requests
from config import channels, messages

import env

channels = channels.Channels
messages = messages.Messages

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel_id = disnake.utils.get(member.guild.channels, name="general")
		channel = self.bot.get_channel(channel_id.id)
		await channel.send(f"Hej debílci, došel {member.mention} tak ho pozdravte. <:feelsWowMan:747845161563979857>")

	@commands.slash_command(name="kredity", description="Prints out credits for BIT")
	async def kredity(self, ctx):
		await ctx.send(messages.kredity)

	@commands.slash_command(name="user", description="Prints out info about user")
	async def user_info(self, ctx, target: disnake.Member = None):
		target = target or ctx.author
		
		headers = {
                    'authorization': env.authorization
                    }
		r = requests.get(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/messages/search?author_id={target.id}&include_nsfw=true', headers=headers)
		data = json.loads(r.text)

		embed = disnake.Embed(title="User information",
					  color=target.color,
					  timestamp=datetime.utcnow())

		if target.avatar is not None:
			embed.set_thumbnail(url=target.avatar)
		print(target.roles)

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

		await ctx.send(embed=embed)

	@commands.slash_command(name="server", description="Prints out info about server")
	async def server_info(self, ctx):
		embed = disnake.Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

		if ctx.guild.icon is not None:
			embed.set_thumbnail(url=ctx.guild.icon)
		
		statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

		fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner.mention, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans().flatten()), True),
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
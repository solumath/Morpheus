import disnake
from disnake.ext import commands

buy = [
	"[Rounds](https://store.steampowered.com/app/1557740/ROUNDS/) - 3,49€",
	"[Garry's Mod](https://store.steampowered.com/app/4000/Garrys_Mod/) - 4,99€",
	"[BattleBlock Theater®](https://store.steampowered.com/app/238460/BattleBlock_Theater/) - 2,99€",
	"[Castle Crashers®](https://store.steampowered.com/app/204360/Castle_Crashers/) - 2,39€",
	"[Magicka 2](https://store.steampowered.com/app/238370/Magicka_2/) - 3,74€",
	"[Worms W.M.D](https://store.steampowered.com/app/327030/Worms_WMD/) - 5,99€",
	"[Stick Fight: The Game](https://store.steampowered.com/app/674940/Stick_Fight_The_Game/) - 2,49€",
	"[PAYDAY 2](https://store.steampowered.com/app/218620/PAYDAY_2/) - 0,99€"
	]

optional = [
	"[Portal 2](https://store.steampowered.com/app/620/Portal_2/) - 0,79€",
	"[Pummel Party](https://store.steampowered.com/app/880940/Pummel_Party/) - 7,49€",
	"[Project Winter](https://store.steampowered.com/app/774861/Project_Winter/) - 7,55€",
	"[Planetary Annihilation: TITANS](https://store.steampowered.com/app/386070/Planetary_Annihilation_TITANS/) - 6,24€",
	"[Deep Rock Galactic](https://store.steampowered.com/app/548430/Deep_Rock_Galactic/) - 14,99€",
	"[Hearts of Iron IV](https://store.steampowered.com/app/394360/Hearts_of_Iron_IV/) - 9,99€",
	"[SpeedRunners](https://store.steampowered.com/app/207140/SpeedRunners/) - 3,74€"
	]
	
class Games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.slash_command(name="games", description="Prints out list of games")
	async def games(self, ctx):
		embed = disnake.Embed(colour=0x30fc03)
		embed.set_author(name="List of games in summer steam sale", icon_url="https://cdn.disnakeapp.com/avatars/722567836010151938/bda3258e4cdd76a2f71f9beda73c2e5b.webp?size=128")
		embed.add_field(name="Must have", value = "\n".join(buy), inline=False)
		embed.add_field(name="Optional", value = "\n".join(optional), inline=False)
		await ctx.send(embed=embed)
	
	@commands.slash_command(name="addgame", description="add game to a list")
	async def add_game(self, ctx, category, name, link, price):
		field = {
					"optional": optional,
					"buy": buy	
				}
		if field.get(category) == None:
			await ctx.send("Category not found")
		else:
			field.get(category).append(f"[{name}]({link}) - {price}")
			await ctx.send("List updated")


def setup(bot):
	bot.add_cog(Games(bot))

import disnake
from disnake.ext import commands
import utility
from config.messages import Messages
from features.restaurants import RestaurantsScraper
import io
import unidecode


restaurants = []
days = ["pondeli", "utery", "streda", "ctvrtek", "patek", "sobota", "nedele", "dnes"]


async def autocomp_restaurants(inter: disnake.ApplicationCommandInteraction, user_input: str):
    return [restaurant for restaurant in restaurants if user_input.lower() in restaurant]


class Restaurants(commands.Cog):
    def __init__(self, bot):
        global restaurants
        self.bot = bot
        self.scraper = RestaurantsScraper()
        restaurants = self.scraper.get_restaurants()

    @commands.slash_command(name="restaurant_menu", description=Messages.restaurant_menu_brief)
    async def get_restaurant_menu(
        self,
        inter: disnake.ApplicationCommandInteraction,
        restaurant: str = commands.Param(autocomplete=autocomp_restaurants)
    ):
        await inter.response.defer()
        await self.print_menu(inter, restaurant)

    @commands.cooldown(rate=1, per=600.0, type=commands.BucketType.user)
    @commands.slash_command(name="restaurants_all", description=Messages.restaurant_all_menus_brief)
    async def get_all_restaurants(
        self,
        inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer()
        restaurants = self.scraper.get_restaurants()
        for restaurant in restaurants:
            await self.print_menu(inter, restaurant)

    async def print_menu(self, inter, restaurant):
        if restaurant in restaurants:
            menu, type = self.scraper.get_menu(restaurant)
            if type == 'file':
                await inter.send(
                    f"Menu z **{restaurant.upper()}**.",
                    file=disnake.File(io.BytesIO(menu), filename=f"{restaurant}.jpg")
                )
            else:
                await inter.send(f"Menu z **{restaurant.upper()}**.")

                # split text to lines to find days and higlight them with markdown
                menu = menu.splitlines()
                aligned_menu = []
                for line in menu:
                    if any(day in unidecode.unidecode(line.strip().lower()) for day in days):
                        line = line.lstrip(" ")
                        aligned_menu.append(f"# {line}")
                    else:
                        aligned_menu.append(line.strip())

                # make list to string again and cut it for sending
                aligned_menu = "\n".join(aligned_menu)
                output = utility.cut_string(aligned_menu, 1950)
                for menu in output:
                    await inter.channel.send(f"```md\n{menu}```")
        else:
            await inter.send("Restaurant nebyl nalezena")


def setup(bot):
    bot.add_cog(Restaurants(bot))

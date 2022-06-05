import disnake
import requests
from datetime import date, time

from disnake.ext import commands, tasks

from config.messages import Messages
from config.channels import Channels


class Nameday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cz_name = ""
        self.sk_name = ""
        self.send_names.start()

    async def _svatek(self):
        url = f"http://svatky.adresa.info/json?date={date.today().strftime('%d%m')}"
        res = requests.get(url).json()
        names = []
        for i in res:
            names.append(i["name"])
        self.cz_name = Messages.name_day_cz.format(name=", ".join(names))
    
    async def _meniny(self):
        url = f"http://svatky.adresa.info/json?lang=sk&date={date.today().strftime('%d%m')}"
        res = requests.get(url).json()
        names = []
        for i in res:
            names.append(i["name"])
        self.sk_name = Messages.name_day_sk.format(name=", ".join(names))
    
    @commands.slash_command(name="svatek", description=Messages.name_day_cz_brief)
    async def svatek(self, inter: disnake.ApplicationCommandInteraction):
        await self._svatek()
        await inter.response.send_message(self.cz_name)

    @commands.slash_command(name="meniny", description=Messages.name_day_sk_brief)
    async def meniny(self, inter: disnake.ApplicationCommandInteraction):
        await self._meniny()
        await inter.response.send_message(self.sk_name)

    @tasks.loop(time= time(5,0))
    async def send_names(self):
        await self._svatek()
        await self._meniny()
        channel = self.bot.get_channel(Channels.name_day)
        await channel.send(f"{self.cz_name}\n{self.sk_name}")


def setup(bot):
    bot.add_cog(Nameday(bot))

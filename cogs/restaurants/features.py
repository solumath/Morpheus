from io import StringIO

import pandas as pd
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class RestaurantsScraper:
    def __init__(self, session: ClientSession):
        self.session = session
        self.urls = {
            "zagreb": "https://zagreb.cz/denni-menu/",
            "nepal": "https://nepalbrno.cz/weekly-menu/",
            "kormidlo": "https://www.ukormidla.cz/menu-pro-plavciky",
            "portoriko": "https://restauraceportoriko.cz/denni-menu/",
            "globus": "https://www.globus.cz/brno/sluzby-a-produkty/restaurace",
        }
        self.restaurants = {
            "zagreb": self.get_zagreb_menu,
            "nepal": self.get_nepal_menu,
            "kormidlo": self.get_kormidlo_menu,
            "portoriko": self.get_portoriko_menu,
            "globus": self.get_globus_menu,
        }

    async def get_soup(self) -> BeautifulSoup:
        async with self.session.get(self.url) as response:
            content = await response.content.read()
        soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
        return soup

    def get_restaurants(self) -> list[str]:
        keys = self.restaurants.keys()
        return list(keys)

    async def get_menu(self, restaurant) -> tuple[bytes, str] | tuple[str, str]:
        if restaurant in self.restaurants:
            return await self.restaurants[restaurant]()
        else:
            raise Exception("Restaurant not found")

    async def get_zagreb_menu(self) -> tuple[bytes, str]:
        self.url = self.urls["zagreb"]
        soup = await self.get_soup()
        images = soup.find_all("img", {"data-permalink": lambda x: x and "denni-menu" in x})
        async with self.session.get(images[0]["src"]) as response:
            image = await response.read()
        return image, "file"

    async def get_nepal_menu(self) -> tuple[str, str]:
        self.url = self.urls["nepal"]
        soup = await self.get_soup()
        table = soup.find_all("table")[2]
        df = pd.read_html(StringIO(str(table)))[0]
        df = df.fillna("")
        text = df.to_string(index=False, header=False)
        return text, "text"

    async def get_kormidlo_menu(self) -> tuple[str, str]:
        self.url = self.urls["kormidlo"]
        soup = await self.get_soup()
        days = ["Pondelí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"]
        divs = soup.find_all("div", {"class": "tydenniMenu"})
        df = pd.DataFrame()

        for index, div in enumerate(divs):
            day = days[index]
            df = pd.concat([df, pd.DataFrame([day])])
            tables = div.find_all("table")
            for table in tables:
                df_table = pd.read_html(StringIO(str(table)))[0]
                df_table = df_table.fillna("")
                df = pd.concat([df, df_table])

        df = df.fillna("")
        text = df.to_string(index=False, header=False)
        return text, "text"

    async def get_portoriko_menu(self) -> tuple[str, str]:
        self.url = self.urls["portoriko"]
        soup = await self.get_soup()
        div = soup.find("div", {"class": "print-menu"})
        table = div.find("table")
        df = pd.read_html(StringIO(str(table)))[0]
        df = df.fillna("")
        text = df.to_string(index=False, header=False)
        return text, "text"

    async def get_globus_menu(self) -> tuple[str, str]:
        self.url = self.urls["globus"]
        soup = await self.get_soup()
        section = soup.find_all("div", {"id": "klasicke-menu"})[0]
        divs = section.find_all("ul")

        df = pd.DataFrame()
        for div in divs:
            li_section = div.find_all("li")
            for menu in li_section:
                day = menu.find("h3").text
                date = menu.find("span").text
                df = pd.concat([df, pd.DataFrame([[day, date]])])
                table = menu.find("table")
                if table:
                    df_table = pd.read_html(StringIO(str(table)))[0]
                    df = pd.concat([df, df_table])

        df = df.fillna("")
        text = df.to_string(index=False, header=False)
        return text, "text"

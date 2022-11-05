from bs4 import BeautifulSoup
import pandas as pd
import requests


class RestaurantsScraper:
    def __init__(self):
        self.urls = {
            'zagreb': 'https://zagreb.cz/denni-menu/',
            'nepal': 'https://nepalbrno.cz/weekly-menu/',
            'kormidlo': 'https://www.ukormidla.cz/menu-pro-plavciky',
            'kotelna': 'http://www.kotelnaopava.cz/',
            'portoriko': 'https://restauraceportoriko.cz/denni-menu/',
            'globus': 'https://www.globus.cz/brno/nabidka/restaurace.html',
        }
        self.restaurants = {
            'zagreb': self.get_zagreb_menu,
            'nepal': self.get_nepal_menu,
            'kormidlo': self.get_kormidlo_menu,
            'kotelna': self.get_kotelna_menu,
            'portoriko': self.get_portoriko_menu,
            'globus': self.get_globus_menu,
        }

    def get_soup(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        return soup

    def get_restaurants(self):
        keys = self.restaurants.keys()
        return list(keys)

    def get_menu(self, restaurant):
        if restaurant in self.restaurants:
            return self.restaurants[restaurant]()
        else:
            raise Exception('Restaurant not found')

    def get_zagreb_menu(self):
        self.url = self.urls['zagreb']
        soup = self.get_soup()
        images = soup.find_all('img', {'data-permalink': lambda x: x and 'denni-menu' in x})
        image = requests.get(images[0]['src']).content
        return image, 'file'

    def get_nepal_menu(self):
        self.url = self.urls['nepal']
        soup = self.get_soup()
        table = soup.find_all('table')[2]
        df = pd.read_html(str(table))[0]
        df = df.fillna('')
        text = df.to_string(index=False, header=False)
        return text, 'text'

    def get_kormidlo_menu(self):
        self.url = self.urls['kormidlo']
        soup = self.get_soup()
        days = ['Pondelí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota', 'Neděle']
        divs = soup.find_all('div', {'class': 'tydenniMenu'})
        df = pd.DataFrame()

        for index, div in enumerate(divs):
            day = days[index]
            df = pd.concat([df, pd.DataFrame([day])])
            tables = div.find_all('table')
            for table in tables:
                df_table = pd.read_html(str(table))[0]
                df_table = df_table.fillna('')
                df = pd.concat([df, df_table])

        df = df.fillna('')
        text = df.to_string(index=False, header=False)
        return text, 'text'

    def get_kotelna_menu(self):
        self.url = self.urls['kotelna']
        soup = self.get_soup()
        images = soup.find_all('img', {'src': lambda x: x and 'Menu' in x})
        image = requests.get(images[0]['src']).content
        return image, 'file'

    def get_portoriko_menu(self):
        self.url = self.urls['portoriko']
        soup = self.get_soup()
        div = soup.find('div', {'class': 'print-menu'})
        table = div.find('table')
        df = pd.read_html(str(table))[0]
        df = df.fillna('')
        text = df.to_string(index=False, header=False)
        return text, 'text'

    def get_globus_menu(self):
        self.url = self.urls['globus']
        soup = self.get_soup()
        divs = soup.find_all('div', {'class': 'restaurant__menu-table-row'})
        df = pd.DataFrame()

        for div in divs:
            day = div.find('p', {'class': 'restaurant__menu-table-day headline'}).text
            date = div.find('p', {'class': 'restaurant__menu-table-date'}).text
            df = pd.concat([df, pd.DataFrame([[day, date]])])
            table = div.find('table', {'class': 'restaurant__menu-food-table'})
            df_table = pd.read_html(str(table))[0]
            df = pd.concat([df, df_table])

        df = df.fillna('')
        text = df.to_string(index=False, header=False)
        return text, 'text'

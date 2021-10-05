from typing import List

import requests
from bs4 import BeautifulSoup

BASE_ARMORY_URL = "https://lostark.game.onstove.com/Profile/Character/%s"


class ArmoryCrawler:
    username: str

    def __init__(self, username: str):
        self.username = username
        r = requests.get(BASE_ARMORY_URL % username)
        self.soup = BeautifulSoup(r.text, 'lxml')

    def get_all_characters_names(self, server: str) -> list:
        characters = {}
        bs_server_list: List[BeautifulSoup] = self.soup.find_all('strong', {'class': 'profile-character-list__server'})
        bs_char_list: List[BeautifulSoup] = self.soup.find_all('ul', {'class': 'profile-character-list__char'})

        for i, bs_server in enumerate(bs_server_list):
            bs_char_per_server = bs_char_list[i].find_all('li')

            characters[bs_server.text.replace('@', '')] = [
                char.find('span').find('span').text
                for char in bs_char_per_server
            ]

        return characters[server]

    def get_characters_item_level(self) -> float:
        bs_item_level_div = self.soup.find('div', {'class': 'level-info2__expedition'}).find_all('span')
        return float(bs_item_level_div[1].text.replace('Lv.', '').replace(',', ''))

    def get_characters_job(self) -> str:
        bs_job_image = self.soup.find('img', {'class': 'profile-character-info__img'})
        return bs_job_image['alt']

from bs4 import BeautifulSoup as bs

from pathlib import Path
import requests, json


site_name = ['https://www.instagram.com/', 'https://www.reddit.com/user/', 'https://github.com/', 'https://career.habr.com/',
'https://pikabu.ru/@']

user_urls = []

n_data = {}


def search_user(): # Search for a page by nickname
    nickname = input("Enter the nickname of the user you want to find: ")

    if nickname != '':
        for s_name in site_name:
            url = f"{s_name}{nickname}/"
            response = requests.get(url)
            page=bs(response.content,'html.parser')
            title=str(page.find('title'))
            if 'instagram' in s_name:
                if nickname.lower() in title:
                    user_urls.append(url)
            else:
                if nickname in title:
                    user_urls.append(url)
        
        n_data[f'{nickname}'] = user_urls
        
        write(n_data, 'data.json')
    else:
        print("You haven't entered a username.\n")
        search_user()


def write(data, filename): # Writing data to a json file
    p = Path(filename)
    if p.stat().st_size <= 0:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    else:
        with open(filename, 'r', encoding='utf-8') as file:
            data_list = json.load(file)

        data_list.update(data)

        sorted_by_nickname = sorted(data_list)
        sorted_data = {nickname: data_list[nickname] for nickname in sorted_by_nickname}

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(sorted_data, file, indent=4)

search_user()
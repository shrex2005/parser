import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def rstua():

    data = []

    url = "https://rst.ua/ukr/oldcars/subaru/"
    agent = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=agent) as rp:
            r = await aiohttp.StreamReader.read(rp.content)
            html = BS(r, 'lxml')
            aps = html.find_all('div', {'class': 'rst-uix-margin'})
            
            for ap in aps:
                lst = ap.find('div', {'class': 'rst-uix-float-left'}).find_all('section', {'class': 'rst-ocb1'})
                for l in lst:
                    announcements = l.find('div', {'class': 'rst-page-wrap'}).find_all('div', {'class': 'rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv'})
                    for ann in announcements:
                        link = ann.find('a', {'class': 'rst-ocb-i-a'}).get('href')
                        title = ann.find('a', {'class': 'rst-ocb-i-a'}).find('h3', {'class': 'rst-ocb-i-h'}).find('span', {'class': ''}).text
                    #prewiev_pic = announcements.find('a', {'class': 'rst-ocb-i-a'}).find('div', {'class': 'rst-ocb-i-i'}).find('img').get('src')
                        print(f'Лінк: https://rst.ua{link}\nЗаголовок: {title}\n')
            # announcements = aps.find('section', {'class': 'rst-ocb1'}).find('div', {'class': 'rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv'})
            # print(announcements)
                # for rst in announcements:
                #     rs = rst.find_all('div', {'class': 'rst-page-wrap'})
                #     print(rs)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rstua())
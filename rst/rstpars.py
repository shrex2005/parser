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
            aps = html.findAll('section', {'class': 'rst-ocb1'})

            for ap in aps:
                announcement1 = ap.find('div', {'class': 'rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv rst-ocb-i-crash'}).find('a', {'class': 'rst-ocb-i-a'}).get('href')
                announcement2 = ap.find('div', {'class': 'rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv'})
                announcement3 = ap.find('div', {'class': 'rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv rst-ocb-i-blue'})
                print(announcement1)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rstua())
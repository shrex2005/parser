import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def rstua():

    fp = 1
    lp = input("Введіть номер сторінки на якій ви хочете завершити: ")

    data = []
    try:
        print(requests.get(f"https://rst.ua/ukr/oldcars/subaru/{lp}.html"))
    except:
        await rstua()
    
    for p in range(int(fp), int(lp) + 1):
        print(p)
        url = f"https://rst.ua/ukr/oldcars/subaru/{p}.html"
        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('div', {'class': 'rst-uix-margin'})
                
                for ap in aps:
                    lst = ap.find('div', {'class': 'rst-uix-float-left'}).find_all('section', {'class': 'rst-ocb1'})
                    for l in lst:                                                                            #rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv
                        announcements = l.find('div', {'class': 'rst-page-wrap'}).find_all('div', {'class': 'rst-ocb-i rst-ocb-i-premium rst-uix-radius roiv'})
                        for ann in announcements:
                            link = ann.find('a', {'class': 'rst-ocb-i-a'}).get('href')
                            title = ann.find('a', {'class': 'rst-ocb-i-a'}).find('h3', {'class': 'rst-ocb-i-h'}).find('span', {'class': ''}).text
                        #prewiev_pic = announcements.find('a', {'class': 'rst-ocb-i-a'}).find('div', {'class': 'rst-ocb-i-i'}).find('img').get('src')
                            print(f'Лінк: https://rst.ua{link}\nЗаголовок: {title}\n')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rstua())
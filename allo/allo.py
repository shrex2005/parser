import sys
import pandas
import asyncio
import aiohttp
import requests
from time import sleep 
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def allo():

    data = []
    
    starturl = 'https://allo.ua/ua/products/notebooks/p-1/'
    agent = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(starturl, headers=agent) as rp:
            re = await aiohttp.StreamReader.read(rp.content)
            html = BS(re, 'lxml')
            maxpage = html.find_all('a', {'class': 'pagination__links'})[4].text   

    fp = input("Введіть номер сторінки з якої ви хочете почати: ")

    try:
        fp = int(fp)
    except ValueError:
        sys.exit("Число не підходить")
    
    lp = input(f"Введіть номер сторінки на якій ви хочете завершити (не більше {maxpage}): ")
    maxpage = int(lp)
    
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Число не підходить")

    if fp > 0 and lp <= maxpage:
        if fp <= lp:   
            for p in range(fp, lp + 1):
                url = f"https://allo.ua/ua/products/notebooks/p-{p}/"
                agent = {'User-Agent': UserAgent().random}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=agent) as rp:
                        r = await aiohttp.StreamReader.read(rp.content)
                        html = BS(r, 'lxml')
                        aps = html.find_all('div', {'class': 'product-card'})

                        for ap in aps:
                            link = ap.find('a', {'class': 'product-card__title'}).get('href')
                            title = ap.find('a', {'class': 'product-card__title'}).get('title')

                            try:
                                feedback_count = ap.find('span', {'class': 'review-button__text review-button__text--count'}).text
                            except Exception:
                                feedback_count = 0

                            try:
                                cur_price = ap.find('div', {'class': 'v-pb__cur'}).find('span', {'class': 'sum'}).text
                                old_price = 'None'
                            except Exception:
                                cur_price = ap.find('div', {'class': 'v-pb__cur discount'}).find('span', {'class': 'sum'}).text
                                old_price = ap.find('div', {'class': 'v-pb__old'}).find('span', {'class': 'sum'}).text
                            
                            characteristic = ap.find('div', {'class': 'product-card__detail'}).find('dd').text


                            print(link, title, cur_price, old_price, characteristic, feedback_count)
                                            

                            data.append([link, title, cur_price, old_price, characteristic, feedback_count])
                        print(f'Данні з {p} сторінки успішно завантаженні')

                        headers = ["Посилання", "Заголовок", "Ціна", "Стара ціна", "Характеристики", "Кількість відгуків"]    # список за яким будуть заповнені верхні колонки датафрейму
                        df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                        df.to_csv('allo/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(allo())
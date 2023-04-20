import sys
import pandas
import asyncio
import aiohttp
import requests
from time import sleep 
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def comfy():

    data = []
    
    starturl = 'https://comfy.ua/ua/notebook/'
    agent = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(starturl, headers=agent) as rp:
            re = await aiohttp.StreamReader.read(rp.content)
            html = BS(re, 'lxml')
            maxpage = html.find_all('a', {'class': 'pagination-item p-i'})

    for mp in maxpage:
        page = mp.text

    fp = input("Введіть номер сторінки з якої ви хочете почати: ")

    try:
        fp = int(fp)
    except ValueError:
        sys.exit("Число не підходить")
    
    lp = input(f"Введіть номер сторінки на якій ви хочете завершити (не більше {page.strip()}): ")
    maxpage = int(lp)
    
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Число не підходить")

    if fp > 0 and lp <= maxpage:
        if fp <= lp:   
            for p in range(fp, lp + 1):
                if p == 1:
                    url = f"https://comfy.ua/ua/notebook/"
                else:
                    url = f"https://comfy.ua/ua/notebook/?p={p}"
                agent = {'User-Agent': UserAgent().random}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=agent) as rp:
                        r = await aiohttp.StreamReader.read(rp.content)
                        html = BS(r, 'lxml')
                        aps = html.find_all('div', {'class': 'products-list-item products-catalog-grid__item products-list-item--grid'})
                        
                        for ap in aps:
                            
                            link = ap.find('a', {'class': 'products-list-item__name'}).get('href')
                            title = ap.find('a', {'class': 'products-list-item__name'}).get('title')

                            try:
                                raiting = ap.find('div', {'class': 'icon-comfy rating-box__active'}).text
                            except Exception:
                                raiting = 'Немає'

                            price = ap.find('div', {'class': 'products-list-item__actions-price-current'}).text
                            

                            try:
                                old_price = ap.find('div', {'class': 'products-list-item__actions-price-old'}).text
                            except Exception:
                                old_price = price

                            try:
                                count_feedbacks = ap.find('a', {'class': 'products-list-item__reviews icon-comfy'}).text
                            except Exception:
                                count_feedbacks = 0

                            try:
                                is_aviable = ap.find('div', {'class': 'products-list-item__annotation-title products-list-item__annotation-out-of-stock'}).text
                            except Exception:
                                is_aviable = 'Є в наявності'                 

                            data.append([link, title, raiting.strip(), old_price.split('\n')[1].strip(), price.split('\n')[1].strip(), count_feedbacks.strip(), is_aviable.strip()])
                        print(f'Данні з {p} сторінки успішно завантаженні')
                        sleep(1)

                        headers = ["Посилання", "Заголовок", "Рейтинг", "Стара ціна", "Теперішня ціна", "Кількість відгуків", "Статус"]    # список за яким будуть заповнені верхні колонки датафрейму
                        df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                        df.to_csv('comfy/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(comfy())
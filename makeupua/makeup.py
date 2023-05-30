import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def autoria():
    starturl = 'https://makeup.com.ua/ua/categorys/20280/'
    agent = {'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession() as session:
        async with session.get(starturl, headers=agent) as rp:
            re = await aiohttp.StreamReader.read(rp.content)
            html = BS(re, 'lxml')
            maxpage = html.find_all('li', {'class': 'page__item'})

    for mp in maxpage:
        page = mp.text

    fp = input("Введіть номер сторінки з якої ви хочете почати: ")

    try:
        fp = int(fp)
    except ValueError:
        sys.exit("Число не підходить")
    pof = fp-1 * 32
    lp = input(f"Введіть номер сторінки на якій ви хочете завершити (не більше {page.strip()}): ")
    maxpage = int(lp)

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    
    for p in range(fp, lp + 1):
        url = f"https://makeup.com.ua/ua/categorys/20280/#offset={pof}"
        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('div', {'class': 'info-product-wrapper'})
                
                for ap in aps:
                    link = "https://makeup.com.ua/" + ap.find('a', {'class': 'simple-slider-list__name'}).get('href')
                    title = ap.find('a', {'class': 'simple-slider-list__name'}).get('data-default-name')
                    try:
                        price = ap.find('div', {'class': 'simple-slider-list__price product-item__price_red'}).find('span', {'class': 'price_item'}).text
                    except:
                        price = ap.find('span', {'class': 'simple-slider-list__price'}).find('span', {'class': 'price_item'}).text

                    data.append([link, title, price])
                print(f'Данні з {p} сторінки успішно завантаженні')
                pof += 32

                headers = ["Посилання", "Назва", "Актуальна ціна"]    # список за яким будуть заповнені верхні колонки датафрейму
                df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                df.to_csv('makeupua/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(autoria())
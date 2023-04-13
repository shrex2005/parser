import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def prom():
    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    for p in range(fp, lp + 1):
        print(f'Данні з {p} сторінки успішно завантаженні')
        url = f"https://prom.ua/ua/Noutbuki;{p}" 
        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('div', {'class': 'l-GwW js-productad'})
                
                for ap in aps:
                    link = ap.find('a', {'class': '_0cNvO jwtUM'}).get('href')
                    title = ap.find('a', {'class': '_0cNvO jwtUM'}).get('title') #bkjEo
                    try:
                        price = ap.find('div', {'class', 'IP36L bkjEo'}).find('span').text
                    except Exception:
                        price = ap.find('div', {'class', 'bkjEo'}).find('span').text
                    shop_link = ap.find('div', {'class': 'M3v0L BXDW- qzGRQ aO9Co'}).find('a', {'class': '_0cNvO jwtUM'}).get('href')
                    shop_name = ap.find('div', {'class': 'M3v0L BXDW- qzGRQ aO9Co'}).find('a', {'class': '_0cNvO jwtUM'}).text
                    try:
                        shop_raiting = ap.find('div', {'class': 'M3v0L BXDW- qzGRQ aO9Co'}).find('span', {'class': '_0cNvO jwtUM OX5sJ XCtBJ'}).text
                    except Exception:
                        try:
                            shop_raiting = ap.find('div', {'class': 'M3v0L BXDW- qzGRQ aO9Co'}).find('span', {'class': '_0cNvO jwtUM OX5sJ XCtBJ'}).text
                        except Exception:
                            shop_raiting = 'None'
                    print(link, title, price, shop_link, shop_name, shop_raiting)
                
                    data.append([f'https://prom.ua{link}', title, price, shop_link, shop_name, shop_raiting])
                headers = ["Посилання", "Заголовок", "Ціна", "Лінк на магазин", "Ім'я магазину", "Рейтинг магазину"]    # список за яким будуть заповнені верхні колонки датафрейму
                df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                df.to_csv('prom/your_table.csv')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(prom())
import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def rozetka():
    data = []
    
    starturl = 'https://rozetka.com.ua/ua/notebooks/c80004/'
    re = requests.get(starturl)
    m = BS(re.text, 'lxml')
    maxpage = m.find_all('a', {'class': 'pagination__link ng-star-inserted'})

    for mp in maxpage:
        page = [mp.text]

    print(f'Максимальна доступна сторінка: {page[:1][0]}')
    fp = input("Введіть номер сторінки з якої ви хочете почати: ")

    try:
        fp = int(fp)
    except ValueError:
        sys.exit("Число не підходить")
    
    lp = input(f"Введіть номер сторінки на якій ви хочете завершити (не більше {page[:1][0]}): ")
    maxpage = int(lp)
    
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Число не підходить")

    if fp > 0 and lp <= maxpage:
        if fp <= lp:   
            for p in range(fp, lp + 1):
                url = f"https://rozetka.com.ua/ua/notebooks/c80004/page={p}/"
                agent = {'User-Agent': UserAgent().random}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=agent) as rp:
                        r = await aiohttp.StreamReader.read(rp.content)
                        html = BS(r, 'lxml')
                        aps = html.find_all('li', {'class': 'catalog-grid__cell catalog-grid__cell_type_slim ng-star-inserted'})
                        
                        for ap in aps:
                            link = ap.find('a', {'class': 'goods-tile__heading ng-star-inserted'}).get('href')
                            title = ap.find('a', {'class': 'goods-tile__heading ng-star-inserted'}).get('title')
                            raiting = ap.find('div', {'class': 'goods-tile__stars ng-star-inserted'}).find('svg').get('aria-label')

                            try:
                                feedback = ap.find('div', {'class': 'goods-tile__stars ng-star-inserted'}).find('span', {'class': 'goods-tile__reviews-link'}).text
                            except Exception:
                                feedback = '0 відгуків'

                            current_price = ap.find('div', {'class': 'goods-tile__prices'}).find('span', {'class': 'goods-tile__price-value'}).text

                            try:
                                old_price = ap.find('div', {'class': 'goods-tile__prices'}).find('div', {'class': 'goods-tile__price--old price--gray ng-star-inserted'}).text
                            except Exception:
                                old_price = current_price 

                            try:
                                status = ap.find('div', {'class': 'goods-tile__availability goods-tile__availability--available ng-star-inserted'}).text
                            except Exception:
                                status = ap.find('div', {'class': 'goods-tile__availability goods-tile__availability--out_of_stock ng-star-inserted'}).text                            

                            data.append([link, title, raiting, feedback, old_price, current_price, status])
                        print(f'Данні з {p} сторінки успішно завантаженні')

                        headers = ["Посилання", "Заголовок", "Рейтинг", "Кількість відгуків", "Стара ціна", "Теперішня ціна", "Статус"]    # список за яким будуть заповнені верхні колонки датафрейму
                        df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                        df.to_csv('rozetka/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rozetka())
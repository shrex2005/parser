import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def autoria():

    re = requests.get("https://tireshop.ua/shini?page=1")
    m = BS(re.text, 'lxml')
    maxpage = m.find_all('a', {'class': 'page-link'})[2].text
    print(f'Максимальна доступна сторінка: {maxpage}')
    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    
    for p in range(fp, lp + 1):
        url = f"https://tireshop.ua/shini?page={p}"
        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('div', {'class': 'd-flex flex-column product__item-content'})
                
                for ap in aps:
                    link = ap.find('div', {'class': 'product__item-content-model mb-1'}).find('a').get('href')
                    title = ap.find('div', {'class': 'product__item-content-model mb-1'}).find('a').get('title')
                    size = ap.find('div', {'class': 'product__item-content-size mb-2'}).find('a').text
                    rating = ap.find('div', {'class': 'w-100 product__rating'}).text
                    price = ap.find('div', {'class': 'product__item-content-footer-price price-grn'}).text

                    data.append([link, title, size, rating, price])
                print(f'Данні з {p} сторінки успішно завантаженні')

                headers = ["Посилання", "Заголовок", "Розмір", "Рейтинг", "Ціна"]    # список за яким будуть заповнені верхні колонки датафрейму
                df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                df.to_csv('tireshop/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(autoria())
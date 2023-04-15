import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def rstua():
    re = requests.get("https://auto.ria.com/uk/legkovie/ford/?page=1.html")
    m = BS(re.text, 'lxml')
    maxpage = m.find('span', {'class': 'page-item dhide text-c'}).text
    print(f'Максимальна доступна сторінка: {maxpage.split("/")[1]}')
    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    
    for p in range(fp, lp + 1):
        print(f'Данні з {p} сторінки успішно завантаженні')
        url = f"https://auto.ria.com/uk/legkovie/ford/?page={p}.html"
        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('section', {'class': 'ticket-item'})
                
                for ap in aps:
                    link = ap.find('a', {'class': 'm-link-ticket'}).get('href')
                    title = ap.find('a', {'class': 'address'}).get('title')
                    try:
                        priceUSD = ap.find('span', {'class': 'bold size22 green'}).text
                    except:
                        priceUSD = ap.find('span', {'class': 'bold green size22'}).text
                    priceUAH = ap.find('span', {'class': 'i-block'}).find('span', {'class': ''}).text
                    mileage = ap.find('li', {'class': 'item-char js-race'}).text
                    engine = ap.find_all('li', {'class': 'item-char'})[2].text
                    box = ap.find_all('li', {'class': 'item-char'})[3].text
                    data.append([link, title, priceUSD, priceUAH, mileage, engine, box])
                headers = ["Посилання", "Заголовок", "Ціна в $", "Ціна в грн", "Пробіг", "Двигун", "Коробка"]    # список за яким будуть заповнені верхні колонки датафрейму
                df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                df.to_csv('autoria/your_table.csv')  


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rstua())
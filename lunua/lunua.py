import sys
import pandas
import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def lunua():

    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    
    for p in range(fp, lp + 1):
        url = f"https://lun.ua/uk/flats/kyiv?page={p}"
        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('div', {'class': 'UIGrid-col-6 UIGrid-col-lg-6 UIGrid-col-md-6 UIGrid-col-xs-6'})

                for ap in aps:

                    link = ap.find('a', {'class': 'PlansCard-link'}).get('href')
                    # address = ap.find('a', {'class': 'UITypography-h3'}).text
                    # print(address)
                    price_in_UAH = ap.find('div', {'class': {'PlansCard-content'}}).find('span').text
                    price_in_USD = ap.find('div', {'class': {'PlansCard-content'}}).find('span', {'class': 'hidden'}).text
                    sqr_m = ap.find('div', {'class': 'PlansCard-area'}).text
                    rooms_count = ap.find('div', {'class': 'PlansCard-area'}).text
                    area = ap.find('div', {'class': 'PlansCard-labels'}).find('div', {'class': 'UILabel -grey-light -small'}).text
                    floors = ap.find_all('div', {'class': 'PlansCard-labels'})[0]
                    floor = str(floors.text).split('Поверх:')[1].strip()

                    data.append([f'https://lun.ua{link}', price_in_UAH, price_in_USD, sqr_m.split()[0], rooms_count.split()[3], area.strip(), floor])
                print(f'Данні з {p} сторінки успішно завантаженні')

                headers = ["Посилання", "Ціна в грн", "Ціна в $", "Площа", "Кількість кімнвт", "Район", "Поверх"]    # список за яким будуть заповнені верхні колонки датафрейму
                df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                df.to_csv('lunua/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(lunua())
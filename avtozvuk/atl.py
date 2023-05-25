import sys
import pandas
import asyncio
import aiohttp
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def avtozvuk():

    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    
    for p in range(fp, lp + 1):
        if p == 1:
            url = 'https://avtozvuk.ua/ua/avtosignalizatsii/c138'
        else:
            url = f'https://avtozvuk.ua/ua/avtosignalizatsii/c138/page{p}'

        agent = {'User-Agent': UserAgent().random}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=agent) as rp:
                r = await aiohttp.StreamReader.read(rp.content)
                html = BS(r, 'lxml')
                aps = html.find_all('div', {'class': 'products-layout__product-item'})
                
                for ap in aps:
                    link = ap.find('a', {'class': 'product-view-title__link'}).get('href')
                    title = ap.find('a', {'class': 'product-view-title__link'}).text

                    try:
                        old_price = ap.find('div', {'class': 'product-view-prices__old-price-number'}).text
                        cur_price = ap.find('div', {'class': 'product-view-prices__base-price-number'}).text
                        cur_currency = ap.find('div', {'class': 'product-view-prices__base-price-currency'}).text
                        old_currency = ap.find('div', {'class': 'product-view-prices__old-price-currency'}).text
                    except Exception:
                        old_price = 'None'
                        cur_price = ap.find('div', {'class': 'product-view-prices__base-price-number'}).text
                        cur_currency = ap.find('div', {'class': 'product-view-prices__base-price-currency'}).text
                        old_currency = ''

                    is_aviable = ap.find('span', {'class': 'product-view-description__icon'}).text
                    code = ap.find('p', {'class': 'product-view-description__code product-view-description__item'}).text

                    data.append([f'https://avtozvuk.ua{link}', title, f'{old_price} {old_currency}', f'{cur_price} {cur_currency}', is_aviable, code])
                print(f'Данні з {p} сторінки успішно завантаженні')

                headers = ["Посилання", "Заголовок", "Стара ціна", "Теперішня ціна", "Наявність", "Код товару"]    # список за яким будуть заповнені верхні колонки датафрейму
                df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                df.to_csv('avtozvuk/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(avtozvuk())
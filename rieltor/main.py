import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def domria():

    data = []

    staturl = "https://rieltor.ua/kiev/flats-rent/?page=1"
    agent = {'User-Agent': UserAgent().random}
    re = requests.get(staturl)
    m = BS(re.text, 'lxml')
    maxp = m.find('li', {'class': 'last'}).find('a', {'class': 'pager-btn'}).text               # ця конструкція дістає максимально доступний номер сторінки з сайту
    fp = input("Введіть номер сторінки з якої ви хочете почати: ")
    try:
        fp = int(fp)
    except ValueError:
        sys.exit("Число не підходить")
    lp = input(f"Введіть номер сторінки на якій ви хочете завершити (не більше {maxp}): ")           # в цьому запиті при кожному старті програми підставляэться актуальна максимально доступна сторінка
    maxp = int(maxp)
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Число не підходить")
    if fp > 0 and lp <= maxp:
        if fp <= lp:
            print("Процес завантаження даних: ")
            for p in range(fp, lp + 1):
                async with aiohttp.ClientSession() as session:
                    url = f"https://rieltor.ua/kiev/flats-rent/?page={p}"  # у цій змінній зберігається посилання на актальну сторінку, яка змінюється з кожним циклом
                    async with session.get(url, headers=agent) as rp:                                             # цей цикл запбезпечує зміну сторінки                
                        r = await aiohttp.StreamReader.read(rp.content)
                        html = BS(r, 'lxml')
                        aps = html.findAll('div', {'class': 'catalog-card'})
                        print(p, "сторінка:")                                              # це я використав для того щоб корситувач бачив етап збору даних

                        for ap in aps:                                                     # цей цикл запбезпечує зміну оголошення
                            link = ap.find('a', {'class': 'catalog-card-media'}).get('href')              # змінна у яку зберігається посилання на оголошення
                            price = ap.find('strong', {'class': 'catalog-card-price-title'}).text         # змінна у яку зберігається орендна плата 
                            address = ap.find('div', {'class': 'catalog-card-address'}).text              # змінна у яку зберігається адреса квартири
                            rooms = ap.find('div', {'class': 'catalog-card-details'}).findAll('span', {'class': ''})[0].text     # змінна у яку зберігається кількість кімнат
                            sizes = ap.find('div', {'class': 'catalog-card-details'}).findAll('span', {'class': ''})[1].text     # змінна у яку зберігаються площы квартири
                            flore = ap.find('div', {'class': 'catalog-card-details'}).findAll('span', {'class': ''})[2].text     # змінна у яку зберігається поверховість будівлі та поверх квартири
                            data.append([link, price, address, rooms, sizes, flore])        # у цей масив зберігаються всі дані для зручного виводу
                    headers = ["Посилання", "Ціна", "Адреса", "Кількість кімнат", "Площа", "Поверх"]    # список за яким будуть заповнені верхні колонки датафрейму
                    df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                    df.to_csv('rieltor/your_table.csv')                                             # конвертація датафрейму у csv таблицю
        else:
            sys.exit("Проміжок не підходить")
    else:
        sys.exit("Число не підходить")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(domria())
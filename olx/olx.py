import sys
import pandas
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def rstua():
    #re = requests.get("https://www.olx.ua/d/uk/transport/legkovye-avtomobili/?currency=UAH")
    #m = BS(re.text, 'lxml')
    #maxpage = m.find('span', {'class': 'page-item dhide text-c'}).text
    #print(f'Максимальна доступна сторінка: {maxpage.split("/")[1]}')
    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Не коректне значення")
    try:
        for p in range(fp, lp + 1):
            print(f'Данні з {p} сторінки успішно завантаженні')
            url = f"https://www.olx.ua/d/uk/transport/legkovye-avtomobili/chevrolet/?currency=UAH&page={p}&search%5Bfilter_float_motor_year%3Afrom%5D=2015"
            agent = {'User-Agent': UserAgent().random}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=agent) as rp:
                    r = await aiohttp.StreamReader.read(rp.content)
                    html = BS(r, 'lxml')
                    aps = html.find_all('div', {'class': 'css-1sw7q4x'})
                    n=0
                    for ap in aps:
                        n += 1
                        print(n)
                        #link = ap.find('a', {'class': 'css-rc5s2u'}).get('href')
                        title = ap.find('h6', {'class': 'css-16v5mdi er34gjf0'}).text
                        price = ap.find('p', {'class': 'css-10b0gli er34gjf0'}).text
                        city = ap.find('p', {'class': 'css-veheph er34gjf0'}).text
                        mileage = ap.find_all('div', {'class': 'css-efx9z5'})[0].text
                        engine = ap.find_all('div', {'class': 'css-efx9z5'})[2].text
                        box = ap.find_all('div', {'class': 'css-efx9z5'})[1].text
                        try:
                            litrs = ap.find_all('div', {'class': 'css-efx9z5'})[3].text
                        except:
                            litrs = '-'
                        
                        data.append([ title, price, city, mileage, engine, litrs, box])
                        print()
                    headers = [ "Заголовок", "Ціна", "Місто та дата", "Пробіг", "Двигун","Об'єм двигуна", "Коробка"]    # список за яким будуть заповнені верхні колонки датафрейму
                    df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                    df.to_csv('olx/your_table.csv')
    except Exception as _ex:
        print(_ex)
          


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(rstua())
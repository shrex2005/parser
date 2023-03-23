import requests
from bs4 import BeautifulSoup as BS
from time import sleep
import pandas
import sys

data = []

staturl = "https://rieltor.ua/kiev/flats-rent/?page=1"
re = requests.get(staturl)
m = BS(re.text, 'html.parser')
maxp = m.find('li', class_ = 'last').find('a', class_ = 'pager-btn').text               # ця конструкція дістає максимально доступний номер сторінки з сайту

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
        for p in range(fp, lp + 1):                                             # цей цикл запбезпечує зміну сторінки
            url = f"https://rieltor.ua/kiev/flats-rent/?page={p}"              # у цій змінній зберігається посилання на актальну сторінку, яка змінюється з кожним циклом
            r = requests.get(url)
            sleep(3)                                                           # затримка необхідна щоб не перенапружувати сервер
            html = BS(r.content, 'html.parser')
            aps = html.findAll('div', class_ = 'catalog-card')
            print(p, "сторінка:")                                              # це я використав для того щоб корситувач бачив етап збору даних

            for ap in aps:                                                     # цей цикл запбезпечує зміну оголошення
                link = ap.find('a', class_ = 'catalog-card-media').get('href')              # змінна у яку зберігається посилання на оголошення
                price = ap.find('strong', class_ = 'catalog-card-price-title').text         # змінна у яку зберігається орендна плата 
                address = ap.find('div', class_ = 'catalog-card-address').text              # змінна у яку зберігається адреса квартири
                rooms = ap.find('div', class_ = 'catalog-card-details').findAll('span', class_= '')[0].text     # змінна у яку зберігається кількість кімнат
                sizes = ap.find('div', class_ = 'catalog-card-details').findAll('span', class_= '')[1].text     # змінна у яку зберігаються площы квартири
                flore = ap.find('div', class_ = 'catalog-card-details').findAll('span', class_= '')[2].text     # змінна у яку зберігається поверховість будівлі та поверх квартири
                data.append([link, price, address, rooms, sizes, flore])        # у цей масив зберігаються всі дані для зручного виводу
        headers = ["Посилання", "Ціна", "Адреса", "Кількість кімнат", "Площа", "Поверх"]    # список за яким будуть заповнені верхні колонки датафрейму
        df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
        df.to_csv('your_table.csv')                                             # конвертація датафрейму у csv таблицю
    else:
        sys.exit("Проміжок не підходить")
else:
    sys.exit("Число не підходить")
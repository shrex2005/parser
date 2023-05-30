import sys
import pandas
import asyncio
import aiohttp
import requests
from time import sleep 
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

async def comfy():

    starturl = 'https://www.ctrs.com.ua/smartfony/'
#    agent = {'User-Agent': UserAgent().random}
#    async with aiohttp.ClientSession() as session:
#        async with session.get(starturl, headers=agent) as rp:
#            re = await aiohttp.StreamReader.read(rp.content)
#            html = BS(re, 'lxml')
#            maxpage = html.find_all('div', {'class': 'pages-0-2-475'})

#    for mp in maxpage:
#        page = mp.text
    re = requests.get(starturl)
    m = BS(re.text, 'lxml')
    maxpage = m.find('a', {'class': 'item-0-2-478'}).text
    print(f'Максимальна доступна сторінка: {maxpage}')
    fp = 1
    lp = int(input("Введіть номер сторінки на якій ви хочете завершити: "))

    data = []
    fp = input("Введіть номер сторінки з якої ви хочете почати: ")

    try:
        fp = int(fp)
    except ValueError:
        sys.exit("Число не підходить")
    
#    lp = input(f"Введіть номер сторінки на якій ви хочете завершити (не більше {page}): ")
#    maxpage = int(lp)
    
    try:
        lp = int(lp)
    except ValueError:
        sys.exit("Число не підходить")

    if fp > 0 and lp <= maxpage:
        if fp <= lp:   
            for p in range(fp, lp + 1):
                if p == 1:
                    url = f"https://www.ctrs.com.ua/smartfony/"
                else:
                    url = f"https://www.ctrs.com.ua/smartfony/page_{p}/"
                agent = {'User-Agent': UserAgent().random}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=agent) as rp:
                        r = await aiohttp.StreamReader.read(rp.content)
                        html = BS(r, 'lxml')
                        aps = html.find_all('div', {'class': 'br10 p8 border-box pr productCardCategory-0-2-264'})
                        
                        for ap in aps:
                            
                            link = ap.find('a', {'class': 'link line-clamp-2 break-word link-0-2-267'}).get('href')
                            title = ap.find('a', {'class': 'link line-clamp-2 break-word link-0-2-267'}).get('title')
                            price = ap.find('div', {'class': 'old-price oldPrice-0-2-295'}).get('data-price')
                            data.append([link, title, price])
                        print(f'Данні з {p} сторінки успішно завантаженні')
                        sleep(1)

                        headers = ["Посилання", "Заголовок", "Рейтинг", "Стара ціна", "Теперішня ціна", "Кількість відгуків", "Статус"]    # список за яким будуть заповнені верхні колонки датафрейму
                        df = pandas.DataFrame(data, columns = headers)                          # конвертація масиву з даними у датафрейм       
                        df.to_csv('comfy/your_table.csv')  

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(comfy())
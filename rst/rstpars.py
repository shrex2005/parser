import requests
from bs4 import BeautifulSoup as BS
from time import sleep 
import pandas
import sys

data = []

staturl = "https://rst.ua/ukr/oldcars/ford/fusion/"
re = requests.get(staturl)
m = BS(re.content, 'lxml')
mpage = m.find('li', class_='active').find('a', class_='').text
print(mpage)



cost = m.find('li', class_='rst-ocb-i-d-l-i').find('strong', class_='rst-ocb-i-d-l-i-b').find('span', class_= 'rst-ocb-i-d-l-i-s rst-ocb-i-d-l-i-s-p').text
print(cost)
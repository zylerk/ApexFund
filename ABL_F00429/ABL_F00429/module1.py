

import requests
from bs4 import BeautifulSoup as bs


response = requests.get('https://www.pycon.kr/2017/')
html = response.text

#print(response.text)

#soup = bs(html, 'html.parser')
soup = bs(html, 'lxml')

title = soup.select('body > div.frontpage > div.onsky > div > div > p')

print(title[0].text)



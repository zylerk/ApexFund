

import requests
from bs4 import BeautifulSoup as bs
from html.parser import HTMLParser

str = 'http://pub.insure.or.kr/Product.do?area=varinsu&wbid=VarInsu&cmd=varfund_info_t2&s_bsns_cd=2&fund_cd=KLVL0200F11&std_dt=2018-01-19&sk=11a0b7cd58d09b689e62293b4490e8d3822483b754cddb91935dc1b8d16aa70'
response = requests.get(str)
html = response.text

#print(response.text)

#soup = bs(html, 'html.parser')
soup = bs(html, 'lxml')

#title = soup.select('body > div.frontpage > div.onsky > div > div > p')
data = soup.select('div.pop_over_table > table.listB > tbody > tr')

#print(data[0].text)

parser = HTMLParser()

for each_data in data:
    #print (each_data.text)
    #parser.feed(each_data)
    sDate = each_data.contents[1].contents[0]
    sNAV = each_data.contents[3].contents[0]
    sPrice = each_data.contents[5].contents[0]
    sReturn = each_data.contents[7].contents[0]





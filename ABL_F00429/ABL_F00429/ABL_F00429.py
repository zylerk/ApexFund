
import datetime
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

#driver = webdriver.Chrome('D:\Google 드라이브\Apps\chromedriver', chrome_options=options)
driver = webdriver.Chrome('D:\Google 드라이브\Apps\chromedriver')
driver.implicitly_wait(3)

addr = 'http://pub.insure.or.kr/Product.do?area=varinsu&wbid=VarInsu&cmd=varfund_list_B&s_bsns_cd=2&scrn_id=UPD200001'
driver.get(addr)

windows = driver.window_handles
driver.switch_to.window(windows[1])
#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
driver.close()
driver.switch_to.window(windows[0])

input_std_dt = driver.find_element_by_css_selector('#std_dt')
input_fund_name = driver.find_element_by_css_selector('#fund_nm')
qry_button = driver.find_element_by_css_selector('#contents > div.search_area > dl > dd.right > span:nth-child(2) > a')

input_std_dt.clear()

date = datetime.datetime.now() + datetime.timedelta(days=-1)
sDate = date.strftime('%Y-%m-%d')
#input_std_dt.send_keys('2018-01-23')
input_std_dt.send_keys(sDate)
input_fund_name.send_keys('팀챌린지')

qry_button.click()
driver.implicitly_wait(3)

for i in range(1, 7):
    sQry = '#tblList_header > tbody > tr:nth-child({}) > td.left > a'.format(i)    
    qry_fund = driver.find_element_by_css_selector(sQry)
    qry_fund.click()

    windows = driver.window_handles
    driver.switch_to.window(windows[1])

    #str = 'http://pub.insure.or.kr/Product.do?area=varinsu&wbid=VarInsu&cmd=varfund_info_t2&s_bsns_cd=2&fund_cd=KLVL0200F11&std_dt=2018-01-19&sk=11a0b7cd58d09b689e62293b4490e8d3822483b754cddb91935dc1b8d16aa70'
    #response = requests.get(str)

    addr = driver.current_url
    addr = addr.replace("t1", "t2")
    driver.get(addr)
    html = driver.page_source
    soup = bs(html, 'lxml')
    data = soup.select('div.pop_over_table > table.listB > tbody > tr')

    for each_data in data:    
        sDate = each_data.contents[1].contents[0]
        sNAV = each_data.contents[3].contents[0]
        sPrice = each_data.contents[5].contents[0]
        sReturn = each_data.contents[7].contents[0]

    driver.close()
    driver.switch_to.window(windows[0])

driver.close()






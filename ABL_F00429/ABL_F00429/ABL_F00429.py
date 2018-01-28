
import datetime
import re
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Database import DB

def UpdateFundInfo(name):
    db = DB()
    db.connect()
    table_fundcode = db.get_fundtable()
    
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
    
    today =  datetime.datetime.now() 
    date = today + datetime.timedelta(days= -2 -today.weekday())
    sDate = date.strftime('%Y-%m-%d')
    #input_std_dt.send_keys('2018-01-23')
    input_std_dt.send_keys(sDate)
    input_fund_name.send_keys(name)
    
    qry_button.click()
    driver.implicitly_wait(3)
    
    list_item = bs(driver.page_source, 'lxml').select('#tblList_header > tbody > tr')
    len_item = len(list_item)

    for i in range(1, len_item+1):
        sQry = '#tblList_header > tbody > tr:nth-child({}) > td.left > a'.format(i)    
        qry_fund = driver.find_element_by_css_selector(sQry)
        qry_fund.click()  # new window open
    
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
    
        #str = 'http://pub.insure.or.kr/Product.do?area=varinsu&wbid=VarInsu&cmd=varfund_info_t2&s_bsns_cd=2&fund_cd=KLVL0200F11&std_dt=2018-01-19&sk=11a0b7cd58d09b689e62293b4490e8d3822483b754cddb91935dc1b8d16aa70'
        #response = requests.get(str)
    
        addr = driver.current_url    
        fundcode = re.search('(?<=fund_cd=)\w+', addr).group(0)
        fundname = table_fundcode.get(fundcode)
        if(fundname == None):
            driver.close()
            driver.switch_to.window(windows[0])
            continue

            
        # asset allocation 정보 저장
        addr = addr.replace("t1", "t3")
        driver.get(addr)
        html2 = driver.page_source
        soup2 = bs(html2, 'lxml')
        structAA = {}
    
        data = soup2.select('#pop_contents > div:nth-of-type(2) > div.width48p.f_right > table > tbody > tr > td')    
        structAA['Equity'] = data[0].contents[0]
        structAA['Bond'] = data[1].contents[0]
        structAA['Fund'] = data[2].contents[0]
        structAA['Cash'] = data[3].contents[0]
        structAA['ETC'] = data[4].contents[0]
        
        data = soup2.select('#pop_contents > div:nth-of-type(3) > div.width40p.f_left.mgnRght8 > table > tbody > tr > td')
        structAA['Domestic_Equity'] = data[5].contents[0]
        structAA['Overseas_Equity'] = data[7].contents[0]
    
        structAA['Domestic_Bond'] = data[9].contents[0]
        structAA['Overseas_Bond'] = data[11].contents[0]
    
        structAA['Domestic_Equity_Mix'] = data[13].contents[0]
        structAA['Overseas_Commodity'] = data[15].contents[0]
        
        structAA['Domestic_Bond_Mix'] = data[17].contents[0]
        structAA['Overseas_REIT'] = data[19].contents[0]
    
        structAA['Domestic_MMF'] = data[21].contents[0]
        structAA['Overseas_ETC'] = data[23].contents[0]
    
        structAA['Domestic_ETC'] = data[25].contents[0]   
        db.update_AA(fundcode,fundname, structAA)
    
        # 주가 정보 저장
        addr = addr.replace("t3", "t2")
        driver.get(addr)
        html = driver.page_source
        soup = bs(html, 'lxml')
        data = soup.select('div.pop_over_table > table.listB > tbody > tr')
           
    
        for each_data in data:    
            sDate = each_data.contents[1].contents[0]
            sNAV = each_data.contents[3].contents[0]
            sPrice = each_data.contents[5].contents[0]
            sReturn = each_data.contents[7].contents[0]
            db.insert_item(fundname, sDate, sNAV, sPrice, sReturn)
    
        
    
        driver.close()
        driver.switch_to.window(windows[0])
    
    driver.close()
    db.close()
    return 
    #return addr, date, db, driver, i, input_fund_name, input_std_dt, options, qry_button, sDate, table_fundcode, windows

UpdateFundInfo('글로벌멀티에셋')
UpdateFundInfo('팀챌린지')





print('complete')





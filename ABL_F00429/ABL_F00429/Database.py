import pymysql
import datetime
import socket
from Base import BaseClass

class DB(BaseClass):    

    def __init__(self, **kwargs):
        self.conn = 0
        self.cursor = 0
        self.last_time = 0        
        self.update_server = socket.gethostname()
        return super().__init__(**kwargs)

    def close(self):
        if self.conn is not 0:
            self.conn.close()
        return    

    def connect(self):
        try:
            #self.conn = pymysql.connect(host='localhost', user='apex', password='tlsgks01#DB', database='F00429', charset='utf8')
            self.conn = pymysql.connect(host='hulis.com', user='apexfund' , password='tlsgks01#M', database='F00429', charset='utf8')

            self.cursor = self.conn.cursor()
            #self.fundtable = self.get_fundtable()
        except:                        
            return self.error('connection error')

        return self.ok()        
    
    def get_fundtable(self):
        if self.cursor == 0:
            return 0
        self.cursor.execute("SELECT * FROM FundCode")
        
        table = {}

        for row in self.cursor._rows:
            table[row[0]] = row[1]
        
        return table

    def get_last_date(self, tbl_name):
        if self.cursor == 0:
            return 0

        sQry = 'select * from {v_tbl} order by Date desc limit 1'.format( v_tbl = tbl_name)
        self.cursor.execute(sQry)
        res = self.cursor.fetchall()
        return self.cursor._rows[0][0]

    def insert_item(self, table, date, nav, price, ret):
        if self.cursor == 0:
            return self.error('connection error: no cursor')                    

        try:
            nav = nav.replace(',', '')
            price = price.replace(',', '')
            sQry = (" insert into {v_tbl} (Date, NAV, Price, Ret) values  "
                "('{v_date}', {v_nav}, {v_price}, {v_ret}  )"
                .format( v_tbl = table, v_date = date, v_nav = nav, v_price = price, v_ret = ret)
                )

            self.cursor.execute(sQry)
            self.conn.commit()
        except:
            return self.error('insert error')                                    

        return self.ok()        

    def update_AA(self, fundcode, fundname, structAA):
        if self.cursor == 0:
            return self.error('connection error: no cursor')                    

        try:            
            sQry = (" update Asset_Allocation set "
                " Equity={v_equity}, Bond={v_bond}, Fund={v_fund}, Cash={v_cash}, ETC={v_etc} "
                ",Domestic_Equity={v_dom_eq}, Domestic_Bond={v_dom_bond}, Domestic_Equity_Mix={v_dom_eq_mix}, Domestic_Bond_Mix={v_dom_bond_mix}"
                ",Domestic_MMF = {v_dom_mmf}, Domestic_ETC={v_dom_etc}, Overseas_Equity={v_over_eq}, Overseas_Bond={v_over_bond}"
                ",Overseas_Commodity={v_over_comdty}, Overseas_REIT={v_over_reit}, Overseas_ETC={v_over_etc}"
                " where Code='{v_code}' "
                .format(v_equity = structAA['Equity'], v_bond=structAA['Bond'], v_fund=structAA['Fund'], v_cash=structAA['Cash'], v_etc=structAA['ETC'],
                        v_dom_eq=structAA['Domestic_Equity'], v_dom_bond=structAA['Domestic_Bond'],v_dom_eq_mix=structAA['Domestic_Equity_Mix'],
                        v_dom_bond_mix=structAA['Domestic_Bond_Mix'],v_dom_mmf=structAA['Domestic_MMF'],v_dom_etc=structAA['Domestic_ETC'],
                        v_over_eq=structAA['Overseas_Equity'],v_over_bond=structAA['Overseas_Bond'],v_over_comdty=structAA['Overseas_Commodity'],
                        v_over_reit=structAA['Overseas_REIT'],v_over_etc=structAA['Overseas_ETC'], v_code=fundcode )
                )

            self.cursor.execute(sQry)
            self.conn.commit()
        except:
            return self.error('update error')                                    

        return self.ok()        

    def insert_price(self, price,  allow_rate = -1):
        #spread = price['BTC']['bithumb']['USD'] / price['BTC']['bittrex']['USD'] - 1
        #gap = price['BTC']['bithumb']['USD'] - price['BTC']['bittrex']['USD']

        state_execute = ("insert into Price (" 
                         "btc_bittrex_usd, btc_bithumb_usd, btc_spread_bittrex_bithumb, btc_gap_bittrex_bithumb, "
                         "eth_bittrex_usd, eth_bithumb_usd, eth_spread_bittrex_bithumb, eth_gap_bittrex_bithumb, "
                         "xrp_bittrex_usd, xrp_bithumb_usd, xrp_spread_bittrex_bithumb, xrp_gap_bittrex_bithumb, "
                         "update_server, fx_usdkrw, cryptowatch_allow_rate) values " 
                         "({v_btc_bittrex_usd:0.3f}, {v_btc_bithumb_usd:0.3f}, {v_btc_spread:0.3f}, {v_btc_gap:0.3f}, "
                         " {v_eth_bittrex_usd:0.3f}, {v_eth_bithumb_usd:0.3f}, {v_eth_spread:0.3f}, {v_eth_gap:0.3f}, "
                         " {v_xrp_bittrex_usd:0.3f}, {v_xrp_bithumb_usd:0.3f}, {v_xrp_spread:0.3f}, {v_xrp_gap:0.3f}, "
                         " '{v_server}', {v_fx_usdkrw} , {v_allow_rate:0.2f} )"
                         .format(v_btc_bittrex_usd=price['BTC']['bittrex']['USD'], v_btc_bithumb_usd=price['BTC']['bithumb']['USD'], 
                                 v_btc_spread=price['BTC']['spread'], v_btc_gap=price['BTC']['gap'], 
                                 
                                 v_eth_bittrex_usd=price['ETH']['bittrex']['USD'], v_eth_bithumb_usd=price['ETH']['bithumb']['USD'], 
                                 v_eth_spread=price['ETH']['spread'], v_eth_gap=price['ETH']['gap'], 
                                 
                                 v_xrp_bittrex_usd=price['XRP']['bittrex']['USD'], v_xrp_bithumb_usd=price['XRP']['bithumb']['USD'], 
                                 v_xrp_spread=price['XRP']['spread'], v_xrp_gap=price['XRP']['gap'], 
                                 
                                 v_server=self.update_server, v_fx_usdkrw = price['usdkrw'] ,v_allow_rate = allow_rate) 
                         )

        if self.cursor == 0:
            return self.error('connection error: no cursor')            

        try:
            self.cursor.execute(state_execute)
            self.conn.commit()
        except:
            return self.error('insert error')                                    

        return self.ok()        

    def select_all(self):
        self.cursor.execute("SELECT * FROM Price order by Time desc")
        res = self.cursor.fetchall()

        for row in self.cursor._rows:
            print(row)
        return



if __name__ == "__main__": 
    # test code

    print('DB test...')

    #conn = pymysql.connect(host='35.200.40.111', user='bap', password='quantum1!', database='bap', charset='utf8')
    #conn = pymysql.connect(host='localhost', user='bap', password='quantum1!', database='bap', charset='utf8')
    #cursor = conn.cursor()
    db = DB()
    db.connect()


    #cursor.execute( "Insert into Price (bittrex_price, bithumb_price, spread, gap) values ( 12345.0, 12350.0, 0.06, 33) " )
    #conn.commit()
    db.insert_price(1231.01, 1313.01)



    #cursor.execute("SELECT * FROM Price order by Time desc")
    #res = cursor.fetchall()

    #for row in cursor._rows:
    #    print(row)
    db.select_all()

    time_now = datetime.datetime.utcnow()
    time_last = db.last_time

    print('now = ', time_now)
    print('last = ', time_last)


    db.close()





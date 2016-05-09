# encoding: utf-8
#---------------------------------------
#   抓取玉山銀行的財報資料，可支援資產負載表(年報、季報)，損益表(年報、季報)，現金流量表(年報，季報)
#   Version : 1.0
#   Author : JMLee
#   Release Data : 2015/03/16
#   Python version : 2.7.9
#---------------------------------------

import requests
from bs4 import BeautifulSoup as bs
from common_function import CommonFunction

class GetFinancialReport(CommonFunction):
    def __init__(self, stockid, url='http://www.esunsec.com.tw/z/zc/zcp/zcpa/zcpa.djhtm?A=5240'):
        #初始化股票號碼以及目標網址，玉山銀行股票資料庫
        self.stockid = stockid
        self.url = url
        #Note that the __init__ method never return a value.\
    
    def get_data(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            res.encoding = 'big5'
            soup = bs(res.text)
            tb = soup.select('table table table')
            tb = tb[0].prettify('utf-8')
        else:
            self.error_log('('+str(self.stockid)+')'+' : open url fail!!!')
            tb = 0
        
        return tb

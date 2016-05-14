# -*- coding: utf8 -*-
#---------------------------------------
#   計算此檔股票的分數，再根據實際測試，加加減減囉!!
#   Version : 0.1
#   Author : JMLee
#   Release Data : 
#   Python version : 2.7.9
#---------------------------------------
#---------------------------------------
# a. 淨利是否為正 1分
# b. 營業現金流是否為正 1分
# c. 資產報酬率是否有超過前年 1分
# d. 盈餘品質 ?? 1分
# e. 長期負債與資產，長期負債下滑得1分，如無負債則總資產增加加一分，乾脆用負債比
# f. 流動比率如果增加 1分
# g. 有無現金增資 1分
# h. 毛利率上升 1分
# i. 資產周轉率是否優於前年 1分
#---------------------------------------
#---------------------------------------
#取用5年的財報資訊算出這4年的分數，然後取平均
#---------------------------------------
##引用函式庫
from financial_save_data import FinancialStatementGet
from common_function import CommonFunction
import pandas as pd
import random

class FinancialScoreCal(CommonFunction):
    def __init__(self, stockid=2330, force_update=0, print_result=0):
        self.stockid = stockid
        self.stockstr = '(' + str(stockid) + ')'
        self.print_result = print_result
        self.savefiledir = 'C:\\MMM\\FinancialData\\'
        self.force_update = force_update
        self.delay = 0
        self.rawreport =[]
        self.interest_items = []
        self.score_items = []
        self.score = []
        self.this_year_score = 0
        self.avg = 0
        self.cal_result = 0
        self.init_success = True;

        #取得財報資料，delay是避免連續大量由網路取得財報資料，被封鎖
        if (self.force_update):
            self.delay = 0
        else:
            self.delay = random.randint(3,8)
            
        fstatement = FinancialStatementGet(self.stockid, self.savefiledir, self.force_update, self.delay)
        if(fstatement.financial_statement_get()): #檢查是否有取得資料成功
            self.sout_out_year_data()
        else:
            self.error_log(self.stockstr +' get data fail.')
            self.init_success = False
    
    def sout_out_year_data(self):
        savefiledir = self.savefiledir + str(self.stockid)
        f = open( savefiledir + '\\' + 'Year_BalanceSheet.txt','r')
        tb = f.read()
        df = pd.read_html(tb,encoding = 'utf-8')
        BalanceSheet = df[0]
        f.close()

        f = open( savefiledir + '\\' + 'Year_ProfitAndLossAccount.txt','r')
        tb = f.read()
        df = pd.read_html(tb,encoding = 'utf-8')
        ProfitAndLossAccount = df[0]
        f.close()
        
        f = open( savefiledir + '\\' + 'Year_CashFlow.txt','r')
        tb = f.read()
        df = pd.read_html(tb,encoding = 'utf-8')
        CashFlow = df[0]
        f.close()
        
        print BalanceSheet, ProfitAndLossAccount, CashFlow

# -*- coding: utf8 -*-
#---------------------------------------
#   檢查是否此股票的財務報表(年報季報 月報?)是否需要更新
#   Version : 1.1
#   Author : JMLee
#   Release Data : 2015/03/29
#   Python version : 2.7.9
#---------------------------------------
#引用函式庫
import datetime, os, time
from financial_report_get import GetFinancialReport
from common_function import CommonFunction

class FinancialStatementGet(CommonFunction):
    def __init__(self, stockid=2330, savefiledir='C:\\MMM\\FinancialData\\', forceupdate=0, delay=2):
        self.stockid = stockid
        self.print_prefix = '('+str(stockid)+') :'
        #self.bank = 'web.tcsc.com.tw'
        self.bank = 'www.esunsec.com.tw'
        #self.savefiledir = 'C:\\MMM\\FinancialData\\' + str(stockid)
        self.savefiledir = savefiledir + str(stockid)
        self.updatelog = self.savefiledir + '\\update_log.txt'
        self.forceupdate = forceupdate
        self.delay = delay
        self.is_report_ok = False #紀錄整個過程是否OK
        self.today = datetime.datetime.today()

    def financial_statement_get(self):
        if (self.forceupdate):
            self.is_report_ok = self.force_update()
        else:
            self.is_report_ok = self.check_update()

        return  self.is_report_ok

    def force_update(self):
        #強制更新，並且覆蓋原有檔案
        is_ok = False
        
        if not os.path.isdir(self.savefiledir):
            os.makedirs(self.savefiledir)

        #取得年報與季報資料
        is_year_ok = self.year_update()
        is_season_ok = self.season_update()

        if (is_year_ok & is_season_ok): #取得的資料正確，存檔
            self.creat_report_dir()
            is_ok = True
        else:
            print '取得資料有異，避免運算錯誤，刪除所有檔案'
            self.error_log(self.print_prefix+': file error, delete all file.')
            os.system('rd /S /Q '+ self.savefiledir)
            is_ok = False    

        return is_ok

    def check_update(self):
        #檢查是否需要更新
        #1. 資料夾不存在，強制更新
        #2. 檔案有誤，強制更新，通常檔案有誤多半是沒有該公司財報，強制在更新一次確定是否真的沒有
        #3. 上述兩條件都不成立，檢查更新日期是否有需要更新
        is_ok = False
        
        #檔案不存在，所以強制更新
        if not os.path.isdir(self.savefiledir):
            os.makedirs(self.savefiledir)
            is_ok = self.force_update()
        elif not self.is_file_exist(): #檔案有的不存在，強制更新
            is_ok = self.force_update()
        else: #進入檢查更新的flow
            is_ok = self.is_need_update()

        return is_ok
    
    def is_file_exist(self):
        is_file_exist = os.path.exists(self.savefiledir+'\\update_log.txt') &\
                        os.path.exists(self.savefiledir+'\\Year_BalanceSheet.txt') &\
                        os.path.exists(self.savefiledir+'\\Year_ProfitAndLossAccount.txt') &\
                        os.path.exists(self.savefiledir+'\\Year_CashFlow.txt') &\
                        os.path.exists(self.savefiledir+'\\Season_BalanceSheet.txt') &\
                        os.path.exists(self.savefiledir+'\\Season_ProfitAndLossAccount.txt') &\
                        os.path.exists(self.savefiledir+'\\Season_CashFlow.txt')
        return is_file_exist
                        
    def is_need_update(self):
        is_year_update_ok = False
        is_season_update_ok = False 

        today = self.today
        #today = datetime.datetime(2022, 4, 2)

        logbuff = []
        f = open(self.updatelog,'r')
        for line in f:
            logbuff.append(line.split())
        f.close()
        
        year_update_time = self.year_update_time_get(logbuff)
        season_update_time = self.season_update_time_get(logbuff)

        #debug
        #year_update_time = ['YEAR_UPDATE_TIME', '2013', '3', '24']
        #season_update_time = ['SEASON_UPDATE_TIME', '2013', '3', '24']
        is_year_update = self.is_year_report_update(year_update_time, today)
        is_season_update = self.is_season_report_update(season_update_time, today)

        if (is_year_update):
            is_year_update_ok = self.year_update()
            if (is_year_update_ok):
                for i in range(0, len(logbuff)):
                    if logbuff[i][0] == 'YEAR_UPDATE_TIME':
                        logbuff[i][1] = str(today.year)
                        logbuff[i][2] = str(today.month)
                        logbuff[i][3] = str(today.day)
            else:
                print '取得資料有異，避免運算錯誤，刪除所有檔案'
                self.error_log(self.print_prefix+': 年報更新異常')
                os.system('rd /S /Q '+savefiledir)
                return False                

        if (is_season_update):
            is_season_update_ok = self.season_update()
            if (is_season_update_ok):
                for i in range(0, len(logbuff)):
                    if logbuff[i][0] == 'SEASON_UPDATE_TIME':
                        logbuff[i][1] = str(today.year)
                        logbuff[i][2] = str(today.month)
                        logbuff[i][3] = str(today.day)
            else:
                print '取得資料有異，避免運算錯誤，刪除所有檔案'
                self.error_log(self.print_prefix+': 季報更新異常')
                os.system('rd /S /Q '+savefiledir)
                return False                

        f = open(self.updatelog,'w')
        for i in range(0, len(logbuff)):
            for j in range(0, len(logbuff[i])):
                f.write(logbuff[i][j]+' ')
            f.write('\r\n')
        f.close()

        return True
    
    def year_update_time_get(self, updatelog):
        for i in range(0, len(updatelog)):
            if updatelog[i][0] == 'YEAR_UPDATE_TIME':
                break
        return updatelog[i]

    def season_update_time_get(self, updatelog):
        for i in range(0, len(updatelog)):
            if updatelog[i][0] == 'SEASON_UPDATE_TIME':
                break
        return updatelog[i]

    def is_year_report_update(self, attrs, today):

        curr_time = time.mktime(today.timetuple())

        #每年財報更新的時間，最晚3月31日
        if (int(attrs[2]) < 4):
            t = datetime.datetime(int(attrs[1]), 4, 1) #log裡面財報必須更新的日期
            updatetime = time.mktime(t.timetuple())
        else:
            t = datetime.datetime(int(attrs[1])+1, 4, 1) #log裡面財報必須更新的日期
            updatetime = time.mktime(t.timetuple())
            
        t = datetime.datetime(int(attrs[1]), int(attrs[2]), int(attrs[3])) #log裡面財報紀錄的更新時間
        logtime = time.mktime(t.timetuple())
        if ((logtime < updatetime)&(curr_time > updatetime)):
            print '年報須更新'
            return True
        else:
            return False
        
    def is_season_report_update(self, attrs, today):
        
        #每年季報更新日期
        #去年第四季 3月31日，跟年報一起發布
        #今年第一季 5月15日
        #今年第二季 8月14日
        #今年第三季 11月14日
        if (int(attrs[2]) < 4):
            s4 = datetime.datetime(int(attrs[1]), 4, 1)
        else:
            s4 = datetime.datetime(int(attrs[1])+1, 4, 1)
        s1 = datetime.datetime(int(attrs[1]), 5, 31)
        s2 = datetime.datetime(int(attrs[1]), 8, 31)
        s3 = datetime.datetime(int(attrs[1]), 11, 30)

        curr_time = time.mktime(today.timetuple())
        
        updatetime = time.mktime(s1.timetuple())
        t = datetime.datetime(int(attrs[1]), int(attrs[2]), int(attrs[3]))
        logtime = time.mktime(t.timetuple())
        if ((logtime < updatetime)&(curr_time > updatetime)):
            print "第1季須更新"
            return True
        
        updatetime = time.mktime(s2.timetuple())
        t = datetime.datetime(int(attrs[1]), int(attrs[2]), int(attrs[3]))
        logtime = time.mktime(t.timetuple())
        if ((logtime < updatetime)&(curr_time > updatetime)):
            print "第2季須更新"
            return True

        updatetime = time.mktime(s3.timetuple())
        t = datetime.datetime(int(attrs[1]), int(attrs[2]), int(attrs[3]))
        logtime = time.mktime(t.timetuple())
        if ((logtime < updatetime)&(curr_time > updatetime)):
            print "第3季須更新"
            return True

        updatetime = time.mktime(s4.timetuple())
        t = datetime.datetime(int(attrs[1]), int(attrs[2]), int(attrs[3]))
        logtime = time.mktime(t.timetuple())
        if ((logtime < updatetime)&(curr_time > updatetime)):
            print "第4季須更新"
            return True

        return False

    def creat_report_dir(self):
        #建立存檔，通常來到這裡應該是取得的資料全數OK了
        if not os.path.isdir(self.savefiledir):
            os.makedirs(self.savefiledir)
            print '建立資料夾 %s' % self.savefiledir
        f = open(self.updatelog,'w')
        f.write('[Finanical Statement]\r\n')
        f.write('YEAR_UPDATE_TIME '+str(self.today.year)+' '+str(self.today.month)+' '+str(self.today.day)+'\r\n')
        f.write('SEASON_UPDATE_TIME '+str(self.today.year)+' '+str(self.today.month)+' '+str(self.today.day)+'\r\n')
        f.close()   

    def year_update(self):
        #更新年表
        print '開始更新年報(' + str(self.stockid) + ')'
        #資產負債年表
        url = 'http://'+ self.bank +'/z/zc/zcp/zcpb/zcpb.djhtm?A='
        report = self.data_save(url, 'Year_BalanceSheet.txt')
        if not (report):
            return False
        #損益年表
        time.sleep(self.delay)
        url = 'http://'+ self.bank +'/z/zc/zcq/zcqa/zcqa.djhtm?A='
        report = self.data_save(url, 'Year_ProfitAndLossAccount.txt')
        if not (report):
            return False
        #現金流量年表
        time.sleep(self.delay)
        url = 'http://'+ self.bank +'/z/zc/zc3/zc3a.djhtm?A='
        report = self.data_save(url, 'Year_CashFlow.txt')
        if not (report):
            return False
        print '年報更新完畢(' + str(self.stockid) + ')'

        return True

    def season_update(self):
        #更新季表
        print '開始更新季報(' + str(self.stockid) + ')'
        #資產負債季表
        time.sleep(self.delay)
        url = 'http://'+ self.bank +'/z/zc/zcp/zcpa/zcpa.djhtm?A='
        report = self.data_save(url, 'Season_BalanceSheet.txt')
        if not (report):
            return False
        #損益季表
        time.sleep(self.delay)
        url = 'http://'+ self.bank +'/z/zc/zcq/zcq.djhtm?A='
        report = self.data_save(url, 'Season_ProfitAndLossAccount.txt')
        if not (report):
            return False
        #現金流量季表
        time.sleep(self.delay)
        url = 'http://'+ self.bank +'/z/zc/zc3/zc3.djhtm?A='
        report = self.data_save(url, 'Season_CashFlow.txt')
        if not (report):
            return False
        print '季報更新完畢(' + str(self.stockid) + ')'
        
        return True

    def data_save(self, url, filename):
        #存檔
        report = self.financial_update(url)
        if (report): #檢查是否連結失敗
            savefile = self.savefiledir + '\\' + filename;
            f = open(savefile,'w')
            f.write(report)
            f.close()
            return True
        else:
            print '取得資料有問題'
            return False

    def financial_update(self, url):
        #呼叫class GetFinancialReport取得財報資料
        report = GetFinancialReport(self.stockid, url)
        return report.get_data()

if __name__ == '__main__':
    pass


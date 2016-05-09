# -*- coding: utf8 -*-
#---------------------------------------
#   一些共用的function
#   Version : 1.0
#   Author : JMLee
#   Release Data : 2015/03/29
#   Python version : 2.7.9
#   ummpy: http://docs.scipy.org/doc/numpy/reference/generated/numpy.std.html
#   scipy: http://scipy-central.org/item/16/2/basic-linear-regression
#---------------------------------------
import datetime
import numpy
from scipy import stats

class CommonFunction:
    def __init__(self):
        pass
    def get_dev(self, a):
        #檢查是否為數字
        for i in range(0, len(a)):
            if not (self.num_check(a[i])):
                return False;
            
        return numpy.std(a)
            
    def get_slope(self, x, y):
        #檢查是否為數字
        for i in range(0, len(x)):
            if not (self.num_check(x[i])):
                return False;
        for i in range(0, len(y)):
            if not (self.num_check(y[i])):
                return False;
            
        X = numpy.array(x)
        Y = numpy.array(y)
        slope, intercept, r_value, p_value, slope_std_error  = stats.linregress(X, Y)
        return slope
    
    def divide_check(self, a, b):
        #檢查是否除0
        result = 0.0
        if b != 0:
            result = a/b
        elif ((a > 0) & (b == 0)):
            result = 999999
        elif ((a < 0) & (b == 0)):
            result = -999999
        return result

    def check_len(self, data):
        #檢查是否有資料
        if (len(data) == 0):
            return False
        else:
            return True

    def error_log(self, mesg):
        today = datetime.datetime.today()
        f = open('C:\\MMM\\FinancialData\\error_log.txt', 'a')
        f.write(today.ctime())
        f.write(' :')
        f.write(mesg)
        f.write('\r\n')
        f.close()
        
    def num_check(self, a):
        try:
            float(a)
            return True
        except ValueError:
            return False
        
    def big5_check(self, a):
        try:
            b = a.decode('big5')
            return b
        except ValueError:
            return False
        
    def utf8_check(self, a):
        try:
            b = a.encode('utf8')
            return b
        except ValueError:
            return False
        
    def data_vaild(self, data, min_v, max_v):
        if (data > max_v):
            return max_v
        elif (data < min_v):
            return min_v
        else:
            return data
        
    def get_cumulative_growth(self, data):
        if (len(data) <= 1):
            return 0
        growth = 0
        for i in range(0, len(data)-1):
            growth += (data[i] - data[i+1])/data[i+1]
        
        growth /= len(data)-1
        
        return growth
    
    def get_item(self, report, item):
        
        for i in range(0,len(report)):
            if (report[i][0] == item):
                break
        if (len(report[i]) == 0):
            return 0
        else:
            return report[i]
    def print_data(self, item, data):
        print '%s\t' %item,
        for i in range(0, len(data)):
            if (i < len(data)-1):
                print '%.2f \t' % data[i],
            else:
                print '%.2d \t' % data[i]    

if __name__=='__main__':
    pass

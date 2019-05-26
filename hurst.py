#coding:utf-8
import math         #log,exp
import numpy as np

#import scipy as sp   ##在numpy基础上实现的部分算法库
import matplotlib.pyplot as plt  ##绘图库
#from scipy.optimize import leastsq  ##引入最小二乘法算法
import copy

from pylab import mpl
from matplotlib.widgets import Cursor
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

class Hurst(object):
    """docstring for Hurst"""
    def __init__(self, Rt):
        super(Hurst, self).__init__()
        self.Rt = copy.deepcopy(Rt)            #整体对数比率序列
        self.N = len(Rt)-1      #个数N
        self.la = []            #A个子序列 每次计算R/S n 都会改变
        self.A = 0              #A的数值
        
        try:
            for i in xrange(self.N):
                self.Rt[i] = math.log(Rt[i+1]) - math.log(Rt[i])       #将时间序列转换为对数比率序列
        except Exception as e:
            print Rt[i]
            print Rt[i+1]
            raise e
            #self.Rt[i] = np.log(self.Rt[i+1]) - np.log(self.Rt[i])
            #self.Rt[i] = self.Rt[i+1] - self.Rt[i]
        del self.Rt[self.N] #下标，n就是最后一个，0是第一个。#删除最后一个多余的。

    def getH(self):
        #用普通最小二乘法计算H指数
        listn = []      #log n 的一组值
        listRs = []     #对应的log R/S的值
        for i in xrange(8, self.N/2+1):
            # if self.N % i  != 0:
            #     break
            listn.append(i)         # n 取4到N/4
            listRs.append(self.getRS(i))      #n对应的R/S
        return np.polyfit(np.log(listn), np.log(listRs), 1)[0]

    def lowH(self):
        #用普通最小二乘法计算H指数
        listn = []      #log n 的一组值
        listRs = []     #对应的log R/S的值
        for i in xrange(10, self.N/2+1):
            # if self.N % i  != 0:
            #     break
            listn.append(i)         # n 取4到N/4
            listRs.append(self.getRS(i))      #n对应的R/S
        return np.polyfit(np.log(listn), np.log(listRs), 1)[0]

    def highH(self):
        #用普通最小二乘法计算H指数
        listn = []      #log n 的一组值
        listRs = []     #对应的log R/S的值
        for i in xrange(2, int(math.log(self.N))+1 ):###1开始不现实
            # if self.N % i  != 0:
            #     break
            listn.append(2**i)         # n 取4到N/4
            listRs.append(self.getRS(2**i))      #n对应的R/S
        return np.polyfit(np.log(listn), np.log(listRs), 1)[0]
        
    def showT(self):
        #用普通最小二乘法计算周期
        listn = []      #log n 的一组值
        listRs = []     #对应的log R/S的值
        listV = []

        for i in xrange(10, self.N/2+1):#!!!!!！！！！除2还是4
            #canshu.append([i, self.getRS(i)])             rs = self.getRS(i)
            listn.append(math.log(i,10))           # n 取4到N/4       !!!!!!!!!!!!!!!!以10为底。
            rs = self.getRS(i)
            listRs.append(math.log(rs,10))      #n对应的R/S
            listV.append(rs/math.sqrt(i))

        logn=np.array(listn)
        logrs=np.array(listRs)
        v = np.array(listV)


        plt.plot(logn, logrs,'b',label='log(R/S)')
        plt.plot(logn, v, 'r',label='V')
        plt.legend(loc='best') #绘制图例
        cursor = Cursor(plt.gca(), horizOn=True, color='y', lw=1)#光标
        #plt.axis([0,40,0,40])     ###横纵坐标的范围，先横后纵
        #plt.title(u'Hurst:'+str(round(k,3)))    #标题，显示Hurst指数，取3位小数
        plt.show()


    def getRS(self, n):
        #长为n的子序列
        #根据n的值，计算对应的R/S
        self.A = self.N // n
        self.la = []    #先分割子序列
        yushu = self.N % n
        for i in xrange(self.A):
            temp = self.Rt[i*n+yushu : i*n+n+yushu] #la的元素是长为n的列表（子序列）  舍掉前面的，旧日子
            self.la.append(temp)

        REa = [ self.jicha(item, n) for item in self.la]     #每个子序列的极差和均值
        RSa = []
        Sa = [np.std(item) for item in self.la] #每个子序列的标准差std。
        
        try:
            for i in xrange(self.A):
                RSa.append( REa[i][0]/Sa[i] )   #每个子序列的重标极差R/S
        except Exception as e:
            print i
            print REa[i][0]
            print Sa[i]
            raise e
        RS = sum(RSa) / self.A          #计算均值，即为分组为n时对应的R/s
        return RS



    def jicha(self, ll, n):
        Ea = sum(ll) / float(n)     #该子序列的均值
        Xka = [ll[0] - Ea,]         #累计离差
        for i in xrange(1, len(ll)):
            Xa = ll[i] - Ea + Xka[i-1]
            Xka.append(Xa)
        Ra = max(Xka) - min(Xka)    #极差
        return [Ra, Ea]
            
    @classmethod
    def qiwang(cls, T):
        listn = []      #log n 的一组值
        listERs = []     #对应的log R/S的值
        for i in xrange(10, T/2+1):
            listn.append(i)         # n 取4到N/4
            listERs.append(cls.getERS(i))      #n对应的R/S
        #存在数组里
        return np.polyfit(np.log(listn), np.log(listERs), 1)[0]


    @classmethod
    def getERS(cls, n):
        #长为n的子序列
        #根据n的值，计算对应的E[R/S]

        a = (n-0.5)/n 
        b = (math.pi/2.0 * n)**(-0.5)
        c = 0.0
        for r in xrange(1,n):#1~n-1
            c += math.sqrt( (n-r)/float(r))
        return a*b*c

        self.A = self.N // n
        self.la = []    #先分割子序列
        yushu = self.N % n
        for i in xrange(self.A):
            temp = self.Rt[i*n+yushu : i*n+n+yushu] #la的元素是长为n的列表（子序列）  舍掉前面的，旧日子
            self.la.append(temp)

        #Ea  = [ sum(item)/float(n) for item in self.la] #每个子序列的均值
        REa = [ self.jicha(item, n) for item in self.la]     #每个子序列的极差和均值
        RSa = []
        Sa = [np.std(item) for item in self.la] #每个子序列的标准差std。
        for i in xrange(self.A):
            RSa.append( REa[i][0]/Sa[i] )   #每个子序列的重标极差R/S
        RS = sum(RSa) / self.A          #计算均值，即为分组为n时对应的R/s
        return RS

def pinghua(ll, n):
    '''对ll数组进行平滑处理，n是平滑窗口值'''
    result = copy.deepcopy(ll)
    for i in xrange(n-1, len(ll)):
        result[i] =  sum( ll[i+1-n:i+1] )/float(n)        #?????????后一个是按照平滑之后的加，还是元数据呢？
        # result[i] =  sum( result[i+1-n:i+1] )/float(n)        #?????????后一个是按照平滑之后的加，还是元数据呢？
    return result
#coding:utf-8
import numpy as np 
#import pylab as pl
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor

import random
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

from hurst import *
from data import *



if __name__ == '__main__':
    Dt_mix = 1  #数据合并倍率， 例如用15分钟合成60分钟，倍率为4
    data = data_tdx2('000001.xls', Dt_mix=Dt_mix)

    #下面是两周赋值周期方式，保留一个，注释另一个
    
    #第一种，10的指数，观察v转折点，最开始的周期赋值方式
    tt =  1.9878   #！！！！！！！！！！！！！！！观察的周期值
    T = int(10**tt+1) + 1 #周期：
    
    #第二种，直接赋值
    #T =  240      #直接赋值

    Num =    600        #计算的H个数，满足 num+T > len(data)   ！！！！！！！！！！！！！
    
    #平滑度设置,两个平滑曲线
    smooth1 = 1
    smooth2 = 1

    L = len(data)
    title = '周期:'+' : '+str(T)
    print L,'*'*20
    # exit()
    if L < T+Num:   
        print T, Num, L
        print '周期：', T 
        print ';计算天数：',Num,';当前数据：',L,'(-',T+Num-L
        print '数据不足'
        exit()

    xl = []
    yH = []
    yPrice = []
    for i in xrange(Num):
        a = Hurst(data[L-T-i : L-i])
        yH.append(a.lowH())
        print i
        xl.append(Num - i)
        yPrice.append(data[L-i-1])

    xl.reverse()    #从后到今天
    yH.reverse()
    yPrice.reverse()
    #yPrice = [math.log(item) for item in yPrice]   #收盘价取对数

    E = Hurst.qiwang(T)
    yE = [E for i in xrange(len(xl))]

    yzzz = [0.5 for i in xrange(len(xl))]

    y20 = pinghua(yH,smooth2)    #平滑度20
    y60 = pinghua(yH,smooth1)    #平滑度60

    fig = plt.figure(1)
    ax1 = plt.subplot(211) # 在图表2中创建子图1
    ax2 = plt.subplot(212) # 在图表2中创建子图2
    plt.sca(ax1)
    plt.title(title)
    plt.plot(xl, yH, label="Hurst", linewidth=1)
    plt.plot(xl, yE, label="期望",  linewidth=1)
    plt.plot(xl, yzzz, label="0.5",  linewidth=1)
    plt.plot(xl, y60,label="平滑1",linewidth=1)
    plt.plot(xl, y20,label="平滑2",linewidth=1)
    #plt.xlim(0, 100)
    # plt.ylim(0,1)
    plt.legend(loc='upper left') #绘制图例

    plt.sca(ax2)
    plt.plot(xl, yPrice)
    plt.xlabel('日期')
    multi = MultiCursor(fig.canvas,(ax1,ax2),color='r',lw=1)

    plt.show()
 

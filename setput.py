#coding:utf-8
from data import *
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

Original_Cost = 0.0 #总成本
Hold = 0    #持仓几手
title = "-定投策略收益"

def main():
    global Hold, Original_Cost, title
    Base_Buy = 10   # 10 手
    average = 60    #watch 3 months
    Cycle = 20      # a month
    # Avg_BL = True
    Avg_BL = False
    data = data_tdx2('2014.xls')
    stragy = 2
    if stragy == 0:
        title = 'const' + title
    elif stragy == 1:
        title = 'MA1' + title
    else:
        title = 'MA2' + title
    if Avg_BL:
        Base_Line = sum(data[:average])/float(average)
    else:
        Base_Line = data[average]
    
    Earn = []   #收益率

    for i, close in enumerate(data):
        #20交易日定投
        #简单策略，固定定投
        if i % Cycle == 0:
            if stragy == 0:
                const_buy(close, Base_Buy)
            elif stragy == 1:
                MeanAdjust_buy_a(close, Base_Buy)
            else:
                MeanAdjust_buy_b(close, Base_Buy)
        #计算收益率
        if Hold == 0 or Original_Cost == 0.0:
            Earn.append(0)
        else:
            Earn.append(100*(Hold * close / Original_Cost - 1))
    show(range(len(data)), data, Earn)

#策略
def const_buy(close, Base_Buy):
    """简单定投，买Base_Buy手。
    """
    global Hold, Original_Cost
    Hold = Hold+ Base_Buy
    Original_Cost += close * Base_Buy

def MeanAdjust_buy_a(close, Base_Buy):
    """简单均值调整定投，根据当前持有均值和close比较，简单调整Base_Buy手。
    """
    global Hold, Original_Cost
    if Hold != 0:
        Mean = Original_Cost / Hold
        if Mean > close:
            Base_Buy += Base_Buy/2
        elif Mean < close:
            Base_Buy -= Base_Buy/2
    Hold = Hold+ Base_Buy
    Original_Cost += close * Base_Buy

def MeanAdjust_buy_b(close, Base_Buy):
    """均值调整定投，根据当前持有均值和close比较的情况调整Base_Buy手。
    """
    global Hold, Original_Cost
    #整个考虑，放大，缩小都不明显
    # if Hold != 0:
    #     x =close / (Original_Cost / Hold)
    #     y = 1/(x*4/3.0 + 2/3.0) + 0.5
    #     Base_Buy = int(Base_Buy * y + 0.5)  #/向上取整
    # Hold = Hold+ Base_Buy
    # Original_Cost += close * Base_Buy
    #分开考虑
    if Hold != 0:
        Mean = Original_Cost/Hold
        x = close/Mean
        if x < 1:#成本高，市价低，亏损，应该多买
            y = 1/(x - 1.25) + 5
        elif x > 2:
            y = 0.5
        else:
            y = 1.5 - 0.5*x
        Base_Buy = int(Base_Buy * y + 0.5)  #/向上取整
    Hold = Hold+ Base_Buy
    Original_Cost += close * Base_Buy
    


  
def show(Xl, Close, Earn):
    global title
    fig = plt.figure(title)
    ax1 = plt.subplot(211)
    plt.plot(Xl, Close, label='收盘价')
    ax1.axhline(y=Close[0], color='#d46061', linewidth=1, label='建仓价位%d'%Close[0])
    plt.legend(loc='upper left')

    ax2 = plt.subplot(212)
    plt.plot(Xl, Earn, label='收益率')
    low, high = min(Earn), max(Earn)
    mean = sum(Earn) / len(Earn)
    ax2.axhline(y=0, color='#d46061', linewidth=1, label='0')
    ax2.axhline(y=low, color='yellow', linewidth=1, label='min=%0.2f'%low)
    ax2.axhline(y=high, color='gray', linewidth=1, label='high=%0.2f'%high)
    ax2.axhline(y=mean, color='green', linewidth=1, label='mean=%0.2f'%mean)
    plt.legend(loc='upper left')
    # plt.ylim(-25, 15)

    multi = MultiCursor(fig.canvas,(ax1,ax2),color='r',lw=1)
    print Earn[-1]
    plt.show()




if __name__ == '__main__':
    main()
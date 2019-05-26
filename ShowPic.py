#coding:utf-8

import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


def show(Close, Earns):
    Xl = range(len(Close))
    name, rate = 0, 1

    fig = plt.figure('定投策略收益率')
    ax1 = plt.subplot(211)
    plt.plot(Xl, Close, label='收盘价')
    ax1.axhline(y=Close[0], color='#d46061', linewidth=1, label='建仓价位%d'%Close[0])
    plt.legend(loc='upper left')
    low, high = 0, 0
    ax2 = plt.subplot(212)
    for Earn in Earns:
        plt.plot(Xl, Earn[rate], label=Earn[name])
        low = min(low, min(Earn[rate]))
        high = max(high, max(Earn[rate]))
    plt.ylim(int(low-5)/5*5, int(high+5)/5*5)   #不同参数比较时固定合理的y坐标范围
    ax2.axhline(y=0, color='#d46061', linewidth=1, label='0')

    # low, high = min(Earn), max(Earn)
    # mean = sum(Earn) / len(Earn)
    # ax2.axhline(y=low, color='yellow', linewidth=1, label='min=%0.2f'%low)
    # ax2.axhline(y=high, color='gray', linewidth=1, label='high=%0.2f'%high)
    # ax2.axhline(y=mean, color='green', linewidth=1, label='mean=%0.2f'%mean)
    plt.legend(loc='upper left')
    # plt.ylim(-25, 15)

    multi = MultiCursor(fig.canvas,(ax1,ax2),color='r',lw=1)
    plt.show()


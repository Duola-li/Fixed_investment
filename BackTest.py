#coding:utf-8
from data import *
from Stragys import *
from ShowPic import show
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


def main():

    Cycle = 20      #定投周期， a month
    data = data_tdx2('2017.xls')
    stragys = [
            Const_Buy(),
            MeanAdjust(),
            MeanAdjust_plus(),
        ]
    
    Earns = []   #收益率

    for i, close in enumerate(data):
        #20交易日定投
        #简单策略，固定定投
        if i % Cycle == 0:
            for s in stragys:
                s.Buy2(close)
        #计算收益率
        for s in stragys:
            s.EarnRateNow(close)
    for s in stragys:
        Earns.append((s.SName, s.Earns))
    
    show(data, Earns)


if __name__ == '__main__':
    main()
#coding:utf-8
#阴阳hurst
from math import log
from data import *
import copy
import numpy as np
import matplotlib.pyplot as plt  ##绘图库
from matplotlib.widgets import MultiCursor
import pylab as pl
pl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
pl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


def main():
    num_task = 6    #图片个数(任务个数，最大为6)
    num = 200   #计算量
    smooth = 10 #平滑度

    #文件名字,和对应周期
    file1, T1 = 'AAAA.xls', 80
    file2, T2 = 'AAAA.xls', 90
    file3, T3 = 'AAAA.xls', 120

    file4, T4 = 'AAAA.xls', 70
    file5, T5 = 'AAAA.xls', 60
    file6, T6 = 'AAAA.xls', 100

    file_list = [file1, file2, file3, file4, file5, file6]
    T_list = [T1, T2, T3, T4, T5, T6]

    names = locals()
    #周期
    for i in range(num_task):
        data = data_tdx(file_list[i])   #改数据文件名字
        T =  T_list[i]  #周期
        L=len(data)
        if L<T+num:
            print 'Number %d :  len=%d, but num+T=%d, not enough.'%(i+1, L, T+num)
            break

        lu, lh, ld, lx, lv = boxh(data, num, T)
        lx.reverse()
        lh3 = pinghua(lh, smooth)
        lu3 = pinghua(lu, smooth)
        ld3 = pinghua(ld, smooth)

        names['fig%s'%i] = plt.figure('%s-%s'%(file_list[i], i))
        names['ax1%s'%i] = plt.subplot(311)
        names['ax2%s'%i] = plt.subplot(312)
        names['ax3%s'%i] = plt.subplot(313)
        plt.sca(names['ax1%s'%i])
        plt.plot(lx, lh, color='blue', label='bh%d'%T_list[i])
        plt.plot(lx, lu, color='orange', )
        plt.plot(lx, ld, color='green', )
        plt.plot(lx, [0.5 for j in lx], 'r')
        plt.title('Origin T:%d' % T)
        plt.legend(loc='best')

        plt.sca(names['ax2%s'%i])
        plt.plot(lx, lh3, color='blue', label='bhs%d'%T_list[i])
        plt.plot(lx, lu3, color='orange', )
        plt.plot(lx, ld3, color='green',)
        plt.plot(lx, [0.5 for j in lx], 'r')
        plt.legend(loc='best')
        plt.sca(names['ax3%s'%i])
        plt.plot(lx, lv)
        names['multi%s'%i] = MultiCursor(names['fig%s'%i].canvas, (names['ax1%s'%i],names['ax2%s'%i],names['ax3%s'%i]), color='r', lw=1)

    plt.show()



def boxh(data, num, T):
    '获取一条box曲线,返回阳,原，阴。逆序的，今天是第0个'
    lh, lu, ld = [], [], []
    lx, lv = [], []
    L = len(data)
    for i in range(num):
        a = BOX(data[L-T-i:L-i])  #倒叙
        # a = BOX(data[L-T-num+1+i:L-num+1+i])    #正序
        hhh = a.getBC()
        lu.append(2-hhh[1])
        ld.append(2-hhh[2])
        lh.append(2-hhh[0])
        lx.append(i)
        lv.append(data[L-i-1])
    return lu,lh,ld, lx, lv

def pinghua(ll, n):
    '''对ll数组进行平滑处理，n是平滑窗口值'''
    result = copy.deepcopy(ll)
    for i in xrange(0, len(ll)-n+1):
        result[i] =  sum( ll[i:i+n+1] )/float(n)     #倒序数列的平滑处理   

    # for i in xrange(n-1, len(ll)):                #正序列的处理
    #     result[i] =  sum( ll[i+1-n:i+1] )/float(n)        #?????????后一个是按照平滑之后的加，还是元数据呢？
    #     # result[i] =  sum( result[i+1-n:i+1] )/float(n)        #?????????后一个是按照平滑之后的加，还是元数据呢？
    return result

class BOX(object):
    """docstring for BOX"""
    def __init__(self, data):
        super(BOX, self).__init__()
        self.data = data
        self.L = len(data)

    def getBC(self, DEBUG=False):
        lR, lR2, lR3, lYR, lYu, lYd = [], [], [], [], [], []
        for i in xrange(1, int(log(self.L, 2))):    #+1, r will be 0, then the yr is -inf,need another count
            r = self.L/2**i
            m = self.L/r
            # print r
            h123 = self.getYR(m, r)
            lYR.append(h123[0])
            lR.append(r)
            if h123[1] != 0.0:
                lYu.append(h123[1])
                lR2.append(r)
            if h123[2] != 0.0:
                lYd.append(h123[2])
                lR3.append(r)
            
        lR = np.log(lR)
        lR2 = np.log(lR2)
        lR3 = np.log(lR3)
        lYR = np.log(lYR)
        lYd = np.log(lYd)
        lYu = np.log(lYu)
        fa = np.polyfit(lR, lYR, 1)
        fau = np.polyfit(lR2, lYu, 1)
        fad = np.polyfit(lR3, lYd, 1)

        if not DEBUG:
            return (-fa[0], -fau[0], -fad[0])    #no Debug,no draw

        fx = np.poly1d(fa)
        fx2 = np.poly1d(fau)
        fx3 = np.poly1d(fad)
        plt.plot(lR, lYR, 'y*')
        plt.plot(lR, fx(lR), 'r', label='D:%0.3f'%fa[0])
        plt.plot(lR2, fx2(lR), 'r', label='D:%0.3f'%fau[0])
        plt.plot(lR3, fx3(lR), 'r', label='D:%0.3f'%fad[0])
        plt.xlim(-2,6)
        plt.ylim(-2,6)
        plt.legend(loc='best')
        plt.show()

    def getYR(self, m, r):
        #m: num of teams.   r: members of a team.
        up, down, total = 0, 0, 0
        yushu = self.L%m
        for i in xrange(m):
            #total += max(data[i*r:i*r+r]) - min(data[i*r:i*r+r])     #last data will kill.  we can use yushu,like hurst.
            temp = max(self.data[yushu+i*r:yushu+i*r+r]) - min(self.data[yushu+i*r:yushu+i*r+r])     #last data will kill.  we can use yushu,like hurst.
            total += temp
            if self.data[yushu+i*r] > self.data[yushu+i*r+r-1]: #last one, need -1
                down += temp
            elif self.data[yushu+i*r] < self.data[yushu+i*r+r-1]:
                up += temp

        return map(lambda x:x/float(r), [total, up, down]) #total/float(r)


if __name__ == '__main__':
    main()
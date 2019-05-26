#coding:utf-8
from K_dadf import *
from data import *

if __name__ == '__main__':

    data = data_tdx('AAAA.xls')   #改数据文件名字
   
    T =  100       #周期
    num =   10   #总个数

    L=len(data)
    print L
    if L<T+num:
        print T, num, L
        print '周期：', T 
        print ';计算天数：',num,';当前数据：',L,'(-',T+num-L
        print '数据不足'
        exit() 
    
    #t = 2.4     #周期，两行
    #T = int(10**t)+1
    a = attack(data,T) #数据，和周期
   
   
    a.huadong(num)         #要计算的个数
    
    #a.huadong(num,True)       #要计算的个数
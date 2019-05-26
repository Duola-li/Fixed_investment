#coding:utf-8
import xlrd
import copy


def data_tdx2(name, location=5, head=2, tail=0, smooth=1, Dt_mix=1):
    #文件名字，数据所在列数，头部空值行数，尾部空值函数
    try:
        data = xlrd.open_workbook(name)
    except Exception as e:
        print 'tdx version.'
        # return data_tdx_origin2(name, location, head, tail, smooth)
        return data_tdx_origin(name, smooth, Dt_mix)
    print 'execl version.'
    table = data.sheets()[0]
    if tail:
        data = table.col_values(location-1)[head:-tail]
    else: 
        data = table.col_values(location-1)[head:] #行数, #递增的
    if Dt_mix>1:
        q = (len(data)-1)%Dt_mix #last one is base
        data = data[q::Dt_mix]

    if smooth>1:
        return pinghua(data, smooth) #返回正序的数据，和wind统一
    return data 


def data_tdx_origin2(name, location=2, head=2, tail=0, smooth=1):
    close = location
    tdx_file = open(name, 'r')
    if tail:
        lines = tdx_file.readlines()[head:-tail]
    else :
        lines = tdx_file.readlines()[head:]
    data = []
    for x in lines:   #去掉开头和最后的无用数据
        data.append( float(x.split()[close]) )
    if smooth>1:
        return pinghua(data, smooth) #返回正序的数据，和wind统一
    return data 


def data_tdx_origin(name='1.xls', smooth=1, Dt_mix=1):
    close = 4
    tdx_file = open(name, 'r')
    lines = tdx_file.readlines()
    data = []
    for x in lines[4:-1]:   #去掉开头和最后的无用数据
        data.append( float(x.split()[close]) )
    #data.reverse()
    if Dt_mix>1:
        q = (len(data)-1)%Dt_mix #last one is base
        data = data[q::Dt_mix]
    if smooth>1:
        return pinghua(data, smooth) #返回正序的数据，和wind统一
    return data #返回正序的数据，和wind统一

def pinghua(ll, n):
    '''对ll数组进行平滑处理，n是平滑窗口值'''
    #处理正序！！
    if n > len(ll):
        print 'smooth too big.'
    result = copy.deepcopy(ll)
    for i in xrange(n-1, len(ll)):
        result[i] =  sum( ll[i+1-n:i+1] )/float(n)        #?????????后一个是按照平滑之后的加，还是元数据呢？
        # result[i] =  sum( result[i+1-n:i+1] )/float(n)        #?????????后一个是按照平滑之后的加，还是元数据呢？
    return result

if __name__ == '__main__':
    print type(data_tdx('AAAA.xls')[0])
    # data_tdx('1.xlsx')
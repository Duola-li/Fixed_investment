#coding:utf-8

class Stragy(object):
    """base Stragy class"""
    def __init__(self, SName='Base_Stragy'):
        super(Stragy, self).__init__()
        self.Original_Cost = 0.0 #总成本
        self.Hold = 0    #持仓几手
        self.SName = SName
        self.Earns = []
        self.Base_Buy = 10

    def Buy(self, close):
        """收盘价买入，策略执行主体"""
        pass

    def Sell(self, close):
        """收盘价卖出，策略执行主体"""
        pass

    def EarnRateNow(self, close):
        """按收盘价计算当前收益率"""
        #计算收益率
        if self.Hold == 0 or self.Original_Cost == 0.0:
            self.Earns.append(0)
            return 0
        else:
            earn = 100*(self.Hold * close / self.Original_Cost - 1)
            self.Earns.append(earn)
            return earn


class Const_Buy(Stragy):
    """简单固定买入策略"""
    def __init__(self):
        super(Const_Buy, self).__init__('Const_Buy')

    def Buy(self, close):
        """收盘价买入，策略执行主体"""
        """简单定投，买Base_Buy手。"""
        self.Hold = self.Hold+ self.Base_Buy
        self.Original_Cost += close * self.Base_Buy

    def Buy2(self, close):
        self.Buy(close)

class MeanAdjust(Stragy):
    """简单均值调整定投"""
    def __init__(self):
        super(MeanAdjust, self).__init__('MeanAdjust')

    def Buy(self, close):
        """收盘价买入，策略执行主体"""
        """简单均值调整定投，根据当前持有均值和close比较，简单调整Base_Buy手。
        """
        Base_Buy = self.Base_Buy
        if self.Hold != 0:
            Mean = self.Original_Cost / self.Hold
            if Mean > close:
                Base_Buy = self.Base_Buy + self.Base_Buy/2
            elif Mean < close:
                Base_Buy = self.Base_Buy - self.Base_Buy/2
        self.Hold = self.Hold+ Base_Buy
        self.Original_Cost += close * Base_Buy
    def Buy2(self, close):
        """收盘价买入，策略执行主体"""
        """均值调整定投，根据当前持有均值和close比较，简单调整Base_Buy手。Base_Buy会自己变化
        """
        Base_Buy = self.Base_Buy
        if self.Hold != 0:
            Mean = self.Original_Cost / self.Hold
            if Mean > close:
                self.Base_Buy = self.Base_Buy + self.Base_Buy/2
            elif Mean < close:
                self.Base_Buy = self.Base_Buy - self.Base_Buy/2
        self.Hold = self.Hold+ self.Base_Buy
        self.Original_Cost += close * self.Base_Buy

class MeanAdjust_plus(Stragy):
    """均值调整定投"""
    def __init__(self):
        super(MeanAdjust_plus, self).__init__('MeanAdjust_plus')

    def Buy(self, close):
        """收盘价买入，策略执行主体"""
        """简单均值调整定投，根据当前持有均值和close比较，简单调整Base_Buy手。
        """
        Base_Buy = self.Base_Buy
        if self.Hold != 0:
            Mean = self.Original_Cost / self.Hold
            x = close/Mean
            if x < 1:#成本高，市价低，亏损，应该多买
                y = 1/(x - 1.25) + 5
            elif x > 2:
                y = 0.5
            else:
                y = 1.5 - 0.5*x
            Base_Buy = int(self.Base_Buy * y + 0.5)  #/向上取整
        self.Hold = self.Hold+ Base_Buy
        self.Original_Cost += close * Base_Buy

    def Buy2(self, close):
        """收盘价买入，策略执行主体"""
        """均值调整定投，根据当前持有均值和close比较，简单调整Base_Buy手。Base_Buy会自己变化
        """
        Base_Buy = self.Base_Buy
        if self.Hold != 0:
            Mean = self.Original_Cost / self.Hold
            x = close/Mean
            if x < 1:#成本高，市价低，亏损，应该多买
                #貌似是放大效果越大越好
                # y = 1/(x - 1.25) + 5
                # y = 1/(x - 1.2) + 6
                y = 1/(x - 7/6.0) + 7
            else:
                #貌似是放大效果越大越好
                #y = b - k*x  #x=1, y =1. b 越大，缩小越明显。
                # y = 1.5 - 0.5*x
                # y = 2-x
                y = 2.5 - 1.5*x     
            y = max(y, 0.3)   
            self.Base_Buy = int(self.Base_Buy * y + 0.5)  #/向上取整
        self.Hold = self.Hold+ self.Base_Buy
        self.Original_Cost += close * self.Base_Buy







class A(object):
    """docstring for A"""
    def __init__(self, arg):
        super(A, self).__init__()
        self.arg = arg
        
    def aa(self):
        print 'aa'
    def bb(self):
        pass

class B(A):
    """docstring for B"""
    def __init__(self, arg):
        super(B, self).__init__(arg)
        
    def bb(self):
        print "bb"

if __name__ == '__main__':
    a = A('a')
    b = B('b')
    a.aa()
    a.bb()
    print '*'*30
    b.aa()
    b.bb()
        
        
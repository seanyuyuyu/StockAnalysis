#!/usr/bin/python  
# coding: UTF-8  
  
"""This script parse stock info"""  
  
import tushare as ts  
import talib as ta
  
def parse(code_list):  
    '''''process stock'''  
    is_buy    = 0  
    buy_val   = []  
    buy_date  = []  
    sell_val  = []  
    sell_date = []  
    df = ts.get_hist_data(STOCK)  
    df=df.sort_index(axis=0)

    ma20 = df[u'ma20']  
    close = df[u'close']  
    rate = 1.0  
    idx = len(ma20)  

    
    angel=ta.EMA(df['close'].values,timeperiod=2)
    evel=ta.EMA((ta.LINEARREG_SLOPE(df['close'].values,21)*20+df['close'].values),timeperiod=42)
    idx=-len(evel)
  
    while idx < -1:  
        idx += 1  
        close_val = close[idx]  
        ma20_val = ma20[idx]  
        
        if angel[idx] > evel[idx]:  
                if is_buy == 0:  
                        is_buy = 1  
                        buy_val.append(close_val)  
                        buy_date.append(close.keys()[idx])  
        elif angel[idx] < evel[idx]:  
                if is_buy == 1:  
                        is_buy = 0  
                        sell_val.append(close_val)  
                        sell_date.append(close.keys()[idx])  
  
    print "stock number: %s" %STOCK  
    print "buy count   : %d" %len(buy_val)  
    print "sell count  : %d" %len(sell_val)  
  
  
    money=10000
    for i in range(len(sell_val)):  
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])  
        yield1=(sell_val[i]-buy_val[i])/buy_val[i]
        money=money*(1+(sell_val[i]-buy_val[i])/buy_val[i])
        print "buy date : %s, sell date: %s, buy price : %.2f,sell price: %.2f, money: %.2f, yield: %.2f%%" %(buy_date[i], sell_date[i],buy_val[i], sell_val[i],money,100*yield1)
        
    if len(sell_val)<len(buy_val):
        i+=1
        print "buy date : %s, buy price : %.2f" %(buy_date[i], buy_val[i]) 

  
    print "rate: %.2f" % rate  
  
if __name__ == '__main__':  
    STOCK = '000697'       ##浦发
    parse(STOCK)  
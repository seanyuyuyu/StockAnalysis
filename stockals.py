#!/usr/bin/python  
# coding: UTF-8  
  
"""This script parse stock info"""  
  
import tushare as ts  
import talib as ta
import smtplib  
from email.mime.text import MIMEText  
import datetime
import pandas as pd 
#import sys
#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
 #   reload(sys)
 #   sys.setdefaultencoding(default_encoding)

#mailto_list=['yuxg139@139.com']           #收件人(列表)  
#mail_host="email-smtp.us-east-1.amazonaws.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
#mail_user="AKIAJX6GFA7H6GOBJ5FA"                           #用户名  
#mail_pass="Ap3U0Nv/38o3OiK+kVvbtYrfklKdPXfpZxyBmDUT8fZn"                             #密码  
#mail_postfix="qq.com"                     #邮箱的后缀，网易就是163.com  
#sendmsg='start:'
#2020/7/6
mailto_list=['yuxg139@139.com']           #收件人(列表)  
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="loglyer1"                           #用户名  
mail_pass="GQWJDUKVWNOJLPOH"                             #密码  GQWJDUKVWNOJLPOH qwe123
mail_postfix="163.com"    
#2020/7/6

def send_mail(to_list,sub,content):  
    #me="StockAnalyst"+"<"+"yuxg"+"@"+mail_postfix+">"  
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    #msg = MIMEText(content,_subtype='plain')  
    msg = MIMEText(content,'plain','gb2312')  
    #msg = MIMEText(content,format,'GB2312') 
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ",".join(to_list)                #将收件人列表以‘；’分隔  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)                            #连接服务器  
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  

def parse(code_list):  
    '''''process stock'''  
    is_buy    = 0  
    buy_val   = []  
    buy_date  = []  
    sell_val  = []  
    sell_date = []  
    df = ts.get_hist_data(STOCK)  
    df=df.sort_index(axis=0)
    global sendmsg,temp,oper

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
  
    print "stock number: %s %s" %(STOCK,NAME) 
    sendmsg=sendmsg+STOCK+' '+NAME+' '
    #print "buy count   : %d" %len(buy_val)  
    #print "sell count  : %d" %len(sell_val)  
  
  
    money=10000
    for i in range(len(sell_val)):  
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])  
        yield1=(sell_val[i]-buy_val[i])/buy_val[i]
        money=money*(1+(sell_val[i]-buy_val[i])/buy_val[i])
        #print "buy date : %s, sell date: %s, buy price : %.2f,sell price: %.2f, money: %.2f, yield: %.2f%%" %(buy_date[i], sell_date[i],buy_val[i], sell_val[i],money,100*yield1)
    
    now = datetime.datetime.now() 
    ndays=datetime.timedelta(days=6)   
    trend='Down'    
    point=''
    if len(sell_val) <  len(buy_val):
        i+=1
        trend='Up'
        temp=temp+5
        print "buy date : %s, buy price : %.2f" %(buy_date[i], buy_val[i])
        bdstr=buy_date[i]
        buydate=datetime.datetime.strptime(bdstr,'%Y-%m-%d')
        delta=now-buydate
        if int(delta.days)<6:
            point='buy: '+buy_date[i]+' '+bytes(buy_val[i])
            #print "point is: %s" %point
        if int(delta.days)<1:  ##如果是当天发生的
            oper=oper+'buy:'+NAME+' '

    else: 
        sdstr=sell_date[i]
        selldate=datetime.datetime.strptime(sdstr,'%Y-%m-%d')
        delta=now-selldate
        if int(delta.days)<6: #比较当前日期和买卖点差5天内，如果是就提示买卖点，now和buydate
            point='sell: '+sell_date[i]+' '+bytes(sell_val[i])
        if int(delta.days)<1:  ##如果是当天发生的
            oper=oper+'sell:'+NAME+' '
    print "Trend is : %s" %trend 
    #print "point is: %s" %point
    #print type(point.encode("gbk"))
    sendmsg=sendmsg+'Trend is : '+trend+' '
    sendmsg=sendmsg+point.encode("gbk")+'\n'

  
    #print "rate: %.2f" % rate  

def append_excel(filename,temp,op):  
    now = datetime.datetime.now()
    dt=now.strftime('%Y-%m-%d')

    df1 = pd.read_excel(filename,'Sheet1')
    df1.loc[df1.shape[0]+1] = {'date':dt,'temperature':temp,'operation':op}

    writer = pd.ExcelWriter(filename)
    ##df1 = pd.DataFrame(data={'date':[dt], 'temp':[2]})
    df1.to_excel(writer,'Sheet1')
    writer.save()  
  
if __name__ == '__main__':  
    stockpool=[['sh','上证指数'],
                ['399300','沪深300'],
                ##['399102','创业板综'],
                ['150019','银华锐进'],
                ['150201','券商B'],
                ['150153','创业板B'],
                ['150330','保险B'],
                ['150210','国企改B'],
                ['150228','银行B'],
                ['150182','军工B'],
                ['150290','煤炭B级'],
                ['150131','医药B'],
                ['150197','有色B'],
                ['150118','房地产B'],
                ['150288','钢铁B'],
                ['150052','沪深300B'],
                ['150172','证券B'],
                ['150270','白酒B'],
                ['150023','深成指B'],
                ['150195','互联网B'],
                ['502050','上证50B'],
                ['159995','芯片ETF'],
                ['000681','视觉中国'],
                ['000697','炼石航空'],
                ['300446','乐凯新材'],
                ['601360','三六零']]

    now = datetime.datetime.now()
    sendmsg='start:'+now.strftime('%Y-%m-%d %H:%M:%S')+'\n'
    temp=0
    oper=''
    for i in range(len(stockpool)):
        STOCK = stockpool[i][0]  
        NAME= stockpool[i][1]    ##浦发
        parse(STOCK)  

    print "sending email..."
    strtemp='stock temperature is:%d\n' %temp
    oper=oper.decode("utf-8")
    append_excel('temperature.xls',temp,oper) ##写入温度记录excel文件，这里要修改为绝对路径，或者是程序判断和脚本同目录下

    sendmsg=strtemp+sendmsg
    sendmsg=sendmsg.decode("utf-8")
    

    ## 2018-5-10 加入记录最近10天的温度功能，先从温度表格中取出最近10天的温度，然后取tail（10），之后转换成字符串，写入到邮件内
    df=pd.read_excel('temperature.xls')
    df=df.tail(10)
    strtemp=df.to_string()
    sendmsg1=sendmsg+strtemp

    print sendmsg
    send_mail(mailto_list,"分析结果"+now.strftime('%Y.%m.%d'),sendmsg1)
    print "email done!"
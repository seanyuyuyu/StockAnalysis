#!/usr/bin/python  
# coding: UTF-8  
  
"""This script parse stock info"""  
  
import tushare as ts  
import talib as ta
import smtplib  
from email.mime.text import MIMEText  
import datetime

#MA30:=EMA(CLOSE,30);
#强弱:EMA(CLOSE,900);
#STICKLINE((MA30>强弱),MA30,强弱,1,0),COLOR0000FF;
#STICKLINE((MA30<强弱),MA30,强弱,1,0),COLOR00FF00;
#H1:=MAX(DYNAINFO(3),DYNAINFO(5));H1赋值:前收盘价和最高价的较大值
#L1:=MIN(DYNAINFO(3),DYNAINFO(6));L1赋值:前收盘价和最低价的较小值
#P1:=H1-L1;
#阻力:L1+P1*7/8,COLOR00DD00;
#支撑:L1+P1*0.5/8,COLOR00DD00;
#现价:CLOSE,COLORWHITE,LINETHICK1;
#STICKLINE(CROSS(支撑,现价),支撑,阻力,1,0),COLORYELLOW;
#DRAWTEXT(LONGCROSS(支撑,现价,2),支撑*1.001,'★B'),COLORYELLOW;{吸}
#DRAWTEXT(LONGCROSS(现价,阻力,2),现价,'★'),COLORRED;{抛};

mailto_list=['yuxg139@139.com']           #收件人(列表)  
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="loglyer"                           #用户名  
mail_pass="qwe123"                             #密码  
mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com  
#sendmsg='start:'

def send_mail(to_list,sub,content):  
    me="StockAnalyst"+"<"+mail_user+"@"+mail_postfix+">"  
    #msg = MIMEText(content,_subtype='plain')  
    msg = MIMEText(content,'plain','gb2312')  
    #msg = MIMEText(content,format,'GB2312') 
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ",".join(to_list)                #将收件人列表以‘；’分隔  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)                            #连接服务器  
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
  
def get_all_price(code_list):  
    '''''process all stock'''  
    global sendmsg
    df = ts.get_realtime_quotes(STOCK)  
    for i in range(len(STOCK)): 
    	H1=max(float(df.ix[i,['pre_close']]),float(df.ix[i,['high']]))
    	L1=min(float(df.ix[i,['pre_close']]),float(df.ix[i,['low']]))
    	P1=H1-L1
    	zl=L1+P1*7/8
    	zc=L1+P1*0.5/8
    	s="code: %s ,sell price: %3.2f ,buy price: %3.2f" %(STOCK[i],zl,zc)
    	sendmsg=sendmsg+s+"\n"
    	print s
  
if __name__ == '__main__':  
    STOCK = ['300446',
    		'300024',
    		'150118',       ##南山铝业  
             '150019',       ##万  科Ａ  
             '150052',       ##吉林敖东  
             '150153',       ##京东方Ａ  
             '600036',       ##招商银行  
             '601166',       ##兴业银行  
             '600298',       ##安琪酵母  
             '600881',       ##亚泰集团  
             '002582',       ##好想你  
             '600750',       ##江中药业  
             '601088',       ##中国神华  
             '000338',       ##潍柴动力  
             '000895',       ##双汇发展  
             '000792']       ##盐湖股份  

    now=datetime.datetime.now()
    sendmsg='start:'+now.strftime('%Y-%m-%d %H:%M:%S')+'\n'

    get_all_price(STOCK)  
    sendmsg1=sendmsg.decode("utf-8")
    #print sendmsg1
    send_mail(mailto_list,"买卖点"+now.strftime('%Y.%m.%d'),sendmsg1)
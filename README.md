tushare.waditu.com

talib安装
$ pip install TA-Lib
出现错误a
talib/common.c:242:28: fatal error: ta-lib/ta_defs.h: No such file or directory
解决
##### Mac OS X


```
$ brew install ta-lib
```


##### Windows


Download [ta-lib-0.4.0-msvc.zip](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-msvc.zip)
and unzip to ``C:\ta-lib``


##### Linux


Download [ta-lib-0.4.0-src.tar.gz](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz) and:
```
$ untar and cd
$ ./configure --prefix=/usr
$ make
$ sudo make install

安装成功后
再运行sudo pip install TA-Lib，成功
Collecting TA-Lib
  Downloading TA-Lib-0.4.10.tar.gz (829kB)
    100% |████████████████████████████████| 839kB 1.6MB/s 
Installing collected packages: TA-Lib
  Running setup.py install for TA-Lib ... done
Successfully installed TA-Lib-0.4.10

import的时候还会出现错误
>>> import talib
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python2.7/dist-packages/talib/__init__.py", line 4, in <module>
    from . import common
ImportError: libta_lib.so.0: cannot open shared object file: No such file or directory
用ln将需要的so文件链接到/usr/lib或者/lib这两个默认的目录下边
ln -s /where/you/install/lib/*.so /usr/lib
sudo ldconfig

按照时间顺序逆序排列
df=df.sort_index(axis=0)

5日均线
ta.EMA(df['close'].values,timeperiod=5)

天使
ta.EMA(df['close'].values,timeperiod=2)
魔鬼
ta.EMA((ta.LINEARREG_SLOPE(df['close'].values,21)*20+df['close'].values),timeperiod=42)

均线的计算方法十分有问题
按照ta.EMA(df['close'].values,timeperiod=5)计算的5日均线是3245.95568318，行情软件是3253
问题找到了，这里用了EMA，行情上的均线缺省是MA

2017.8.15
修改了通达信的macd指标，使之能显示天使和魔鬼的数值
明天对比两个计算公式结果
20.17.8.16
证明数据是正确的，可以通过脚本自动判断买卖点发邮件或微信公众号文章
首先跟踪各个重点指数和分级基金
2017.8.17
‘sh’ 上证指数
‘399300’ 沪深300
'399102’ 创业板综
‘150019’银华锐进
‘150021’券商B
‘150153’创业板B
‘150222’中航军B
’150210’国企改B
‘150228’银行B
‘150182’军工B
‘150290’煤炭B级
‘150131’医药B
‘150197’有色B

2017.8.20
网易邮箱自动发送邮件有问题

授权码：qwe123

2017.8.22
sendmsg=sendmsg+point+'\n’
报错：
UnicodeEncodeError: 'ascii' codec can't encode characters in position 29-32: ordinal not in range(128)
经过检测，发现point是unicode类型，和sendmsg的ascii类型不能自动转换
#import sys
#default_encoding = 'utf-8'
#if sys.getdefaultencoding() != default_encoding:
 #   reload(sys)
 #   sys.setdefaultencoding(default_encoding)
把缺省编码变为utf8，这里ok，但发邮件又出现问题
强制手工转换：
sendmsg=sendmsg+point.encode("gbk")+'\n’
问题解决

2017-8.24
邮件乱码的解决
首先把ascii转换成unicode
sendmsg1=sendmsg.decode("utf-8")
    print sendmsg
    send_mail(mailto_list,"分析结果",sendmsg1)
然后把发送邮件的内容编码变为gb2312
msg = MIMEText(content,'plain','gb2312') 
问题解决

9.20 buypoint.py 开始
目标：建立一个日内买卖点的提示程序，在10：30或11：00给出日内T的买卖点价位
公式：
#MA30:=EMA(CLOSE,30);
#强弱:EMA(CLOSE,900);
#STICKLINE((MA30>强弱),MA30,强弱,1,0),COLOR0000FF;
#STICKLINE((MA30<强弱),MA30,强弱,1,0),COLOR00FF00;
#H1:=MAX(DYNAINFO(3),DYNAINFO(5));
#L1:=MIN(DYNAINFO(3),DYNAINFO(6));
#P1:=H1-L1;
#阻力:L1+P1*7/8,COLOR00DD00;
#支撑:L1+P1*0.5/8,COLOR00DD00;
#现价:CLOSE,COLORWHITE,LINETHICK1;
#STICKLINE(CROSS(支撑,现价),支撑,阻力,1,0),COLORYELLOW;
#DRAWTEXT(LONGCROSS(支撑,现价,2),支撑*1.001,'★B'),COLORYELLOW;{吸}
#DRAWTEXT(LONGCROSS(现价,阻力,2),现价,'★'),COLORRED;{抛};

当天历史分笔
>>> df=ts.get_today_ticks('300446')
[Getting data:]####################>>> df.head(10)
       time  price pchange  change  volume  amount type
0  15:00:03  29.45   +1.27   -0.03     203  597835   卖盘
1  14:57:03  29.48   +1.38    0.00       0       0   买盘
2  14:57:00  29.48   +1.38    0.00       4   11792   买盘
3  14:56:57  29.48   +1.38    0.00      29   85492   买盘
4  14:56:42  29.48   +1.38    0.00       5   14740   买盘
5  14:56:39  29.48   +1.38    0.00      44  129712   买盘
6  14:56:30  29.48   +1.38    0.00       1    2948   买盘
7  14:56:24  29.48   +1.38    0.00      10   29480   买盘
8  14:56:21  29.48   +1.38    0.00       6   17688  中性盘
9  14:56:15  29.48   +1.38    0.00       7   20636   卖盘

实时分笔
>>> df=ts.get_realtime_quotes('300446')
>>> df.head(10)
   name    open pre_close   price    high     low     bid     ask   volume  \
0  乐凯新材  29.000    29.080  29.450  29.550  28.970  29.450  29.460  1521175   

         amount   ...      a2_p a3_v    a3_p a4_v    a4_p a5_v    a5_p  \
0  44530504.000   ...    29.470  183  29.480  152  29.490   71  29.500   

         date      time    code  
0  2017-09-20  15:05:03  300446  

[1 rows x 33 columns]
>>> df[[‘code','name','price','bid','ask','volume','amount','time']]
     code  name   price     bid     ask   volume        amount      time
0  300446  乐凯新材  29.450  29.450  29.460  1521175  44530504.000  15:05:03

历史分笔可以看到很多笔数据，实时分笔只能看到最近的一笔数据
看起来应该用历史分笔，如果他能够给出到目前时间点的数据

获取数据
>>> df.ix[0,1]
u'29.000'
>>> df.ix[0,'low']
u'28.970'
>>> df.ix[0,'pre_close']
u'29.080'
>>> i=df.ix[0,'pre_close']
>>> print i
29.080
>>> print i*j
29.08029.080
获取后类型为object，不能直接运算，要进行转换
>>> k=float(i)
>>> print k
29.08
>>> print k*2
58.16
>>> print k*j
58.16


10.12
sklearn需要大于50以上的样本
regression线性回归可以跟踪给出预测，应在新股涨幅的预测比较好

10.16
新股数据：
newstock.cfi.cn
建立100个新股样本，存入newstock.xls文件

10.17
审视下金融股，如果进入防守，沪深两市的投资标的
深平安银行 沪杭州银行

读入newstock.xlsx数据
* 
import pandas as pd   
* import numpy as np  
*   
* # 读入数据  
* data=pd.DataFrame(pd.read_excel('000.xlsx',index=False))  
* print(data)  
* 

取到target
>>> y=data[u'破板涨幅'].values
>>> y
array([ 1.495,  2.328,  1.211,  2.327,  1.62 ,  1.962,  1.856,  1.888,
        2.753,  2.627,  1.946,  2.828,  2.479,  2.593,  3.446,  2.98 ,
        1.252,  1.245,  4.973,  3.751,  1.661,  1.733,  1.999,  3.773,
        2.2  ,  5.532,  1.954,  6.869,  3.452,  3.31 ,  4.664,  2.242,
        2.69 ,  2.628,  2.589,  2.283,  2.069,  2.823,  4.991,  2.69 ,
        2.923,  2.333,  2.579,  3.964,  3.71 ,  5.584,  6.268,  1.528,
        2.009,  0.679,  0.825,  0.937,  0.823,  1.057,  0.858,  1.236,
        1.009,  4.826,  1.471,  1.219,  0.943,  0.846,  0.988,  1.884,
        0.669,  1.233,  0.78 ,  0.695,  2.353,  0.901,  1.527,  2.457,
        2.109,  1.735,  1.197,  5.782,  3.932,  1.697,  5.341,  1.684,
        1.067,  6.851,  1.994,  1.859,  0.971,  1.035,  1.04 ,  2.68 ,
        1.15 ,  1.503,  1.666,  2.29 ,  1.694,  2.121,  1.05 ,  1.864,
        2.018,  1.909,  2.023,  1.047,  2.637])
>>> y.shape
(101,)

新股涨停板预测程序nstockpd.py，执行结果
使用scale 准确率14%
不使用scale 准确率9%
但手工测试了几个最后几个数据，误差很小，明天继续测试


2018/2/9 刷新邮件发送服务器为aws ses
mailto_list=['yuxg139@139.com']           #收件人(列表)  
mail_host="email-smtp.us-east-1.amazonaws.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="AKIAIYSX6N4VNK4JM2WA"                           #用户名  
mail_pass="AnnsgD0qfK3VSFnkRHjj8fOph3zMXi3P1Zsa+pAljFZs"                             #密码  
mail_postfix="qq.com"                     #邮箱的后缀，网易就是163.com  
#sendmsg='start:'

def send_mail(to_list,sub,content):  
    me="StockAnalyst"+"<"+"yuxg"+"@"+mail_postfix+">"  
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

2018.3.5 代码上lambda
1、先在ec2上下载本地部署包
pip install lxml -t .
2、用zip格式打包
zip -r ../r01.zip *
3、上传到s3
aws s3 cp r01.zip s3:\\seanyuyuyu.com

3.13 增加股市温度，temp值，为各个指数up的数量和，共20个指数，每个5分，满分100

为了跟踪每天的股市温度，看出是升温还是降温，特地要写一个excel文件，将温度记录下来
写入excel主要通过pandas构造DataFrame，调用to_excel方法实现。
DataFrame.to_excel(excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, encoding=None, inf_rep='inf', verbose=True, freeze_panes=None)
'''
该函数主要参数为:excel_writer。
excel_writer:写入的目标excel文件，可以是文件路径、ExcelWriter对象;
sheet_name:被写入的sheet名称，string类型，默认为'sheet1';
na_rep:缺失值表示，string类型;
header:是否写表头信息，布尔或list of string类型，默认为True;
index:是否写行号，布尔类型，默认为True;
encoding:指定写入编码，string类型。
'''
import pandas as pd
writer = pd.ExcelWriter('output.xlsx')
df1 = pd.DataFrame(data={'col1':[1,1], 'col2':[2,2]})
df1.to_excel(writer,'Sheet1')
writer.save()

df中在末尾插入数据
df.loc[df.shape[0]+1] = {'ds':strToDate('2017-07-21'),'y':0}

dataframe的构造我还要看下，要构造类似：日期 温度 这样的值对，以后还可以用pandas绘制曲线
dataframe写入日期测试结果:
>>> import datetime
>>> now = datetime.datetime.now()
>>> dt=now.strftime('%Y-%m-%d')
>>> dt
'2018-03-13'
>>> df1 = pd.DataFrame(data={'col1':[dt], 'col2':[2]})
>>> df1
         col1  col2
0  2018-03-13     2
可能dt这里不用【】
两种方法选一种:
1. df.to_csv, 参数mode='a'表示追加
2. 
df.to_excel，在写入之前把df的值拼在一起写入，比如原来的数据是df1, 要写入的数据是df2

则 pandas.concat([df1, df2]).to_excel()




3.14 画折线图
首先读出数据到df
df=pd.read_excel(filename)
然后处理df，建立日期索引
df_t=df.set_index(‘date’)
引入plt库
import matplotlib.pyplot as plt
df_t[‘temperature’].plot()
显示折线图
plt.show()


3.15 服务器发现报错，找不到xls文件，因为cron运行时不是在当前目录，这个问题要解决
    with open(filename, "rb") as f:
IOError: [Errno 2] No such file or directory: 'temperature.xls'
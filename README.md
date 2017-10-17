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


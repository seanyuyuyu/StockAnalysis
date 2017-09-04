# StockAnalysis

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

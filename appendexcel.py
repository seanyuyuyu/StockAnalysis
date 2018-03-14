#!/usr/bin/python  
# coding: UTF-8  
  
"""This script parse stock info"""  
  
import pandas as pd 
import datetime
  
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
    STOCK = '000697'       ##浦发
    append_excel('temperature.xls',85,'sell:quanshangB') 
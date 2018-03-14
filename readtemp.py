#!/usr/bin/python  
# coding: UTF-8  
  
"""This script parse stock info"""  
  
import pandas as pd 


   
  
if __name__ == '__main__':  
    df=pd.read_excel('temperature.xls')
    print df


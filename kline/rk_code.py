#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/7/15 
@desc:利用tushare 将股票代码及相关信息输入数据库
'''
# import lib
from urllib.parse import quote_plus as urlquote
import tushare as ts
from goto import with_goto
pro = ts.pro_api('b766c3a415fa6499f12b73d983ee2cdb73da80e293415dff508b60b9')

data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

import pandas as pd
from sqlalchemy import create_engine
from tools.config import config_h
host=config_h.get_config('Mysql_stock','host')
user=config_h.get_config('Mysql_stock','user')
password=config_h.get_config('Mysql_stock','password')
db=config_h.get_config('Mysql_stock','db')
connstr = "mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" % (user,urlquote(password),host,db)
print(connstr)
yconnect = create_engine(connstr, echo=True, max_overflow=5)

# pd.io.sql.to_sql(data,'kline_stock_code_datetr',yconnect, schema='hamob',if_exists='append', chunksize=1000, index=False)
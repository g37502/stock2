#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/7/30 
@desc:
'''
# import lib
'''
key:test_task_list
value: 'code:date'
'''
import redis
aaa=[123,456]
from tools.raids_h import rehis_h3
from tools.mysql_tool import mysql_19
import pandas as pd
# index = pd.date_range('6/1/2021','8/1/2021')
sql = 'select ts_code,list_date from kline_stock_code_datetr'
# print(index)
def tick_task(sql):
	task_list_test=[]
	codes=mysql_19.operation(sql)
	codes = codes.fetchall()
	for code,date in codes:
		print(date,code)
		value = str(date) + ':' + code
		print(value)
		rehis_h3.lpush('tick_task_list', value)

if __name__ == '__main__':
	tick_task(sql)

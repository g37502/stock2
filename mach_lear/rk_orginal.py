#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/2 
@desc:
'''
# import lib
import sys,os
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir)
import pandas as pd
import datetime
from tools.raids_h import rehis_h,rehis_h3
from tools.log_ctrl import logger
from kline.rk_code import yconnect
from kline.get_history_transactions_original_test import get_nextday_kday,get_history_data,data_arran
# index = pd.date_range('7/3/2006','30/6/2021')
def rk_original(task_name):
	'''入库操作或者跳过，判断后一天的涨幅超过1.094 入'''



	task_name_completed = task_name + '_completed'
	while True:
		task =  rehis_h3.spop(task_name)
		if rehis_h3.sismember(task_name_completed,task):
			continue
		code,date =task.split(':')
		rehis_h3.sadd(task_name_completed, task)
		date = date.strip(" ")
		w = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
		if w == 6 or w == 0:
			logger.warn('%s没有数据' %date)
			continue
		# code_list = code.strip(" ").split('.')
		# code = code_list[1].lower() + '.' +code_list[0]
		grow_rate,total_hands = get_nextday_kday(date, code)
		if grow_rate:
			history_data = get_history_data(date, code) #获取数据
		else:
			logger.warn('%s,%s明天没有数据' % (date,code))
			continue
		if history_data:
			data = data_arran(history_data, date, code) #数据整理
		else:
			logger.warn('%s,%s未获得数据' % (date,code))
			continue

		if grow_rate >= 1.094:
			pd.io.sql.to_sql(data,'kline_lmint_sec_deal_original',yconnect, schema='hamob',if_exists='append', chunksize=1000, index=False)
			# logger.debug('明天涨停股')
			# date = str(date).split()[0]
			logger.info('%s,%s,涨停股 , 入库完成' %(code,date))
		else:
			pd.io.sql.to_sql(data,'kline_sec_deal_original',yconnect, schema='hamob',if_exists='append', chunksize=1000, index=False)
			# date = str(date).split()[0]
			# logger.debug('明天没有涨停')
			logger.info('%s,%s, 普通股,入库完成' %(date,code))


if __name__ == '__main__':
	rk_original('tick_task')
#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/10 
@desc:
'''
# import lib
import pandas as pd
from tools.log_ctrl import logger
from tools.mysql_tool import mysql_19
from mach_lear.data_proc import get_nump
from mach_lear.data_proc import get_total_hands
from tools.mysql_tool import mysql_19
from tools.rk_code import yconnect
from tools.raids_h import rehis_h


def write_data(date,code, data, file):

	total_hands = get_total_hands(date,code)

	data['volume'][data['nature'] == '卖盘'] = data['volume'] * -1
	data['time'] = pd.to_timedelta(data['time'])
	data['volume'] = pd.to_numeric(data['volume'])
	data=data.groupby(by=['time'])['volume'].sum()
	data=pd.DataFrame(data)
	data['volume'] = data['volume'] / total_hands
	logger.debug(data.shape)
	# s.set_index('time',inplace=True)
	logger.debug('索引首位是%s,末尾是%s' % (data.index[0],data.index[-1]))


	start1 = '09:25:00'
	start2 = '12:59:00'
	df_time1= pd.timedelta_range(start=start1, periods=7560, freq='1S')
	df_time2 = pd.timedelta_range(start=start2, periods=6720, freq='1S')
	df_time = df_time2.append(df_time1)
	df_time = pd.DataFrame(df_time)
	df_time['volume']=0
	df_time.set_index(0, inplace=True)

	data3 = data + df_time
	data3 = data3['volume'].fillna(0)
	logger.debug(data.shape)

	start3 = '14:51:00'
	index3 = pd.timedelta_range(start=start3, periods=700, freq='1S')
	data3 = data3.drop(index3,errors='ignore')
	data3=pd.DataFrame(data3)
	logger.debug(data3.shape)

	data4 = data3.values.reshape(1,14280)
	data4 = pd.DataFrame(data4)

	data4.to_csv(file, sep=',',mode='a',index=False,header=False)

def publish_task(task_name,sql):
	task_completed = 'task_completed'
	result = mysql_19.operation(sql)
	result = result.fetchall()
	for code,date,count in result:
		task = code + ':' +date
		if rehis_h.sismember(task_completed,task):
			continue
		rehis_h.sadd(task_name,task)

def receive_task(task_name):
	# task_completed = task_name+'_'+'completed'
	task_completed = 'task_completed'
	logger.debug(task_name)
	task = rehis_h.spop(task_name)
	logger.debug(task)
	if rehis_h.sismember(task_completed, task):
		print('重复任务')
		return 1
	rehis_h.sadd(task_completed, task)
	task = task.split(':')
	logger.debug(task)
	return task[0], task[1]

# sql1='select code,DATE_FORMAT(date,"%Y-%m-%d") date,DATE_FORMAT(date,"%H:%i:%S") time,volume,nature from kline_lmint_sec_deal_original where date=%s and code=%s' % (date,code)
# sql2='select code,DATE_FORMAT(date,"%Y-%m-%d") date,DATE_FORMAT(date,"%H:%i:%S") time,volume,nature from kline_sec_deal_original where date=%s and code=%s' % (date,code)

'''录入数据'''
def Input_data(task_table,file = 'text.csv',task_name = 'task_usually' ):

	'''发布任务'''
	# date='2021-07'
	# sql='select code,DATE_FORMAT(date,"%Y-%m-%d") date from kline_lmint_sec_deal_original where DATE_FORMAT(date, "%Y-%m") ="2021-07"'
	# sql1='select code,DATE_FORMAT(date,"%Y-%m-%d") date from kline_sec_deal_original where DATE_FORMAT(date, "%Y-%m") ="2021-07"'
	#
	# publish_task('task_usually',sql)

	try:
		code,date = receive_task(task_name)
		logger.debug('%s%s' % (code,date))
		sql2 = f'select code,DATE_FORMAT(date,"%Y-%m-%d") date,DATE_FORMAT(date,"%H:%i:%S") time,volume,nature from {task_table} where DATE_FORMAT(date,"%Y-%m-%d")=\"{date}\" and code=\"{code}\"'
		# data = mysql_19.operation(sql2)
		data = pd.read_sql_query(sql2, yconnect)
		write_data(date, code, data, file)
	# print(code,date[0],type(data))
	except Exception as e:
		print(f'{e},重复任务or空任务')





if __name__ == '__main__':
	while True:
		Input_data(file='usually.csv',task_table='table')




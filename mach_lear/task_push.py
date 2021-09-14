#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/20 
@desc:
'''
# import lib

from tools.mysql_tool import mysql_19
from tools.raids_h import rehis_h3

######把已完成的原始数据标识放入redis
sql = '''select code as code, DATE_FORMAT(date,'%Y-%m-%d') as date from kline_lmint_sec_deal_original  
UNION 
select code as code,  DATE_FORMAT(date,'%Y-%m-%d') as date from kline_sec_deal_original '''

task_name = 'exit_original_task'
from tools.log_ctrl import logger

def task_set(sql,task_name):
	result = mysql_19.operation(sql)
	result = result.fetchall()
	for code,date in result:
		task = code + ':' + str(date)
		logger.debug(task)
		if rehis_h3.sismember('exit_original_task',task):
			continue
		rehis_h3.sadd(task_name,task)

if __name__ == '__main__':
	task_set(sql, task_name)
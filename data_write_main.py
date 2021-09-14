#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
@auhor: gyl
@file: .py
@data: 2021/8/20 
@desc:
'''
# import lib
import sys
from mach_lear.data_write import Input_data
from tools.config import config_h
##usualy数据
# task_table='kline_sec_deal_original'
# task_name='task_usually'
# file='usually.csv'

##limit数据
# task_table='kline_lmint_sec_deal_original'
# task_name='task_limit'
# file='limit.csv'

##usualy_test数据
# task_table='kline_sec_deal_original'
# task_name='task_usually_test'
# file='usually_test.csv'

##limit_test数据
# task_table='kline_lmint_sec_deal_original'
# task_name='task_limit_test'
# file='limit_test.csv'

task_name = sys.argv[1]
if 'test' in task_name:
	task_name = task_name.replace('_test','')
	task_table = config_h.get_config(task_name, 'task_table')
	file = config_h.get_config(task_name, 'file')
	front,after = file.split('.')
	file = front +'_test.' + after
else:
	task_table = config_h.get_config(task_name,'task_table')
	file = config_h.get_config(task_name, 'file')



if __name__ == '__main__':
	while True:
		Input_data(task_table=task_table, task_name=task_name, file=file)


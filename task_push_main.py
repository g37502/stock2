#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/23 
@desc:
'''
# import lib
import sys
from mach_lear.task_push import task_set
from tools.config import config_h



###任务set模式为’sz.000001:2017-02-23‘

######把已完成的原始数据标识放入redis
# sql = '''select code as code, DATE_FORMAT(date,'%Y-%m-%d') as date from kline_lmint_sec_deal_original
# UNION
# select code as code,  DATE_FORMAT(date,'%Y-%m-%d') as date from kline_sec_deal_original '''
#
# task_name = 'exit_original_task'
#运行方法 python task_push_main.py exit_original_task

#####发布获取原始数据任务
# sql = 'select ts_code,list_date from kline_stock_code_datetr'
# task_name='tick_task'
#运行方法 python task_push_main.py tick_task

# #####发布生成普通数据原始列表
# sql = '''select CODE ,DATE_FORMAT(date,"%Y-%m-%d") from kline_sec_deal_original GROUP BY CODE, DATE_FORMAT(date,"%Y-%m-%d")'''
# task_name = 'usually_task'
#运行方法 python task_push_main.py usually_task

#####发布生成limit原始数据列表
# sql = 'select CODE ,DATE_FORMAT(date,"%Y-%m-%d") from kline_lmint_sec_deal_original GROUP BY CODE, DATE_FORMAT(date,"%Y-%m-%d")'
# task_name='limit_task'
#运行方法 python task_push_main.py limit_task


task_name = sys.argv[1]
sql = config_h.get_config(task_name,'sql')


if __name__ == '__main__':
	task_set(sql,task_name)
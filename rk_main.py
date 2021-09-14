#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/20 
@desc: 将历史逐笔成交存入数据库
python rk_makn.py 'tick_task'
'''
# import lib
import sys
from mach_lear.rk_orginal import rk_original


task_name = sys.argv[1]

if __name__ == '__main__':
	rk_original(task_name)
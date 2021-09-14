#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/9/14 
@desc:
'''
# import lib
from tools.config import config_h
from mach_lear.operdata import output
if __name__ == '__main__':
	path_model= config_h.get_config('mach_lear', 'path_model')
	path_file= config_h.get_config('mach_lear','path_file')
	output(path_model,path_file)

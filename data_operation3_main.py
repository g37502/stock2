#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/25 
@desc:
'''
# import lib
import sys
from mach_lear.data_proc3 import data_operation
import tensorflow as tf
import os
# n_cpus = os.cpu_count()
#
# sess = tf.Session(config=tf.ConfigProto(
#     device_count={ "CPU": n_cpus },
#     inter_op_parallelism_threads=n_cpus,
#     intra_op_parallelism_threads=n_cpus,
# ))



file1=sys.argv[1]
file2=sys.argv[2]
file3 = sys.argv[3]
file4 = sys.argv[4]

if __name__ == '__main__':
	data_operation(file1=file1,file2=file2,file3=file3,file4=file4)
#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/5 
@desc:
'''
# import lib
import pandas as pd
import tensorflow as tf
# sh.000007:2020-07-22改为sh600003
s = 'sh.000007:2020-07-22'
#http://market.finance.sina.com.cn/transHis.php?symbol=sh000011&date=2012-09-12&page=1
import numpy as np
import os
from tools.config import config_h
from tools.log_ctrl import logger

def get_ten(file):
	detail_df = pd.read_csv(file,header=None)
	detail_df = pd.DataFrame(detail_df)
	# detail_df.drop(columns=['id'], inplace=True)
	nuar = np.array(detail_df)
	nuar = tf.convert_to_tensor(nuar, dtype=tf.float32)
	return nuar

def get_mode(path):
	model_dict={}
	for root,dirs,files in os.walk(path):
		for file in files:
			data=get_ten(os.path.join(path,file))
			model_dict[file]=data
	return model_dict

def output(path_model,path_file):
	model_dict = get_mode(path_model)
	w1=model_dict['w1']
	w1=tf.reshape(w1,[14280,256])
	print(w1.shape)
	b1=model_dict['b1']
	w2=model_dict['w2']
	w2=tf.reshape(w2,[256,128])
	b2=model_dict['b2']
	w3=model_dict['w3']
	w3=tf.reshape(w3,[128,2])
	b3=model_dict['b3']
	nuar_test = get_ten(path_file)
	total_correct, total_num = 0, 0

	func = config_h.get_config('mach_lear', 'func')
	for x in nuar_test:

		x = tf.reshape(x, [1, 14280])
		print(x.shape)
		h1 = eval(f'tf.nn.{func}(x@w1 + b1)')
		h2 = eval(f'tf.nn.{func}(h1@w2 + b2)')
		out = h2 @ w3 + b3
		prob = tf.nn.softmax(out, axis=1)
		pred = tf.argmax(prob, axis=1)
		pred = tf.cast(pred, dtype=tf.int32)
		# print('这个是pred2：',pred)
		# y: [b]
		# [b], int32
		# print(pred.dtype, y.dtype)
		# correct = tf.cast(tf.equal(pred, y), dtype=tf.int32)
		# # print('这个是y:', y)
		# correct = tf.reduce_sum(correct)
		# total_correct += int(correct)
		# # print('x.shape[0]:',x.shape[0])
		# total_num += x.shape[0]
		out_num=np.array(out)[0][0]
		logger.info('out_num的值是:%s' % out_num)


if __name__ == '__main__':
	path= '../model/1631595253'
	output(path)

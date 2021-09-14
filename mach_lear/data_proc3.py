#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/8/4 
@desc:
'''
# import lib
import sys
import numpy as np
import pandas as pd
import  tensorflow as tf
import numpy as np
import time,os
from tools.log_ctrl import logger
from tools.config import config_h

sql1='select code,DATE_FORMAT(date,"%Y-%m-%d") date,DATE_FORMAT(date,"%H:%i:%S") time,volume,nature from kline_lmint_sec_deal_original'
sql2='select code,DATE_FORMAT(date,"%Y-%m-%d") date,DATE_FORMAT(date,"%H:%i:%S") time,volume,nature from kline_sec_deal_original'

# sql2 = 'select code,date,volume,nature from kline_sec_deal_original'
# sql1 = 'select code,date,volume,nature from kline_lmint_sec_deal_original'

def get_df(file):
	detail_df = pd.read_csv(file,header=None)
	detail_df = pd.DataFrame(detail_df)
	# detail_df.drop(columns=['id'], inplace=True)
	return detail_df


def get_nump(file1,file2):
	detail_df = get_df(file1)
	detail_df_limit = get_df(file2)
	nuar = np.array(detail_df)
	nuar_limit = np.array(detail_df_limit)
	x1, y1 = nuar.shape
	x2, y2 = nuar_limit.shape
	logger.debug('55555',x1,y1,x2,y2)
	x1 = np.zeros(x1)
	x2 = np.ones(x2)
	nuar = np.vstack((nuar, nuar_limit))
	y = np.hstack((x1, x2))
	return nuar,y
def save_mode(dir,w1,b1,w2,b2,w3,b3):
	dir_root = config_h.get_config('mach_lear','dir')
	dir = os.path.join(dir_root,dir)
	if not os.path.exists(dir):
		os.makedirs(dir)
	w1_tmp=np.array(w1)
	w1_tmp.tofile(f'{dir}/w1', sep=',')
	b1_tmp = np.array(b1)
	b1_tmp.tofile(f'{dir}/b1', sep=',')
	w2_tmp= np.array(w2)
	w2_tmp.tofile(f'{dir}/w2', sep=',')
	b2_tmp= np.array(b2)
	b2_tmp.tofile(f'{dir}/b2', sep=',')
	w3_tmp= np.array(w3)
	w3_tmp.tofile(f'{dir}/w3', sep=',')
	b3_tmp= np.array(b3)
	b3_tmp.tofile(f'{dir}/b3', sep=',')


# logger.debug(pd.timedelta_range(start='09:00:00',periods=30,freq='1S'))
def data_operation(file1,file2,file3,file4):
	stddev = config_h.get_float('mach_lear', 'step_size')
	func = config_h.get_config('mach_lear', 'func')
	batch = config_h.get_int('mach_lear','batch')
	nuar,y = get_nump(file1,file2)
	logger.debug('学习数据集为：', nuar.shape,y.shape)
	nuar = tf.convert_to_tensor(nuar,dtype=tf.float32)
	logger.debug(nuar.shape)
	y = tf.convert_to_tensor(y,dtype=tf.int32)
	# train_db = tf.data.Dataset.from_tensor_slices((nuar,y)).batch(128)
	train_db = tf.data.Dataset.from_tensor_slices((nuar,y))
	train_db = train_db.shuffle(256)
	train_db = train_db.batch(batch)
	train_db = train_db.repeat(1000)
	logger.debug('train_db类型为:',type(train_db))
	train_iter =iter(train_db)
	sample = next(train_iter)
	logger.debug('batch:', sample[0].shape, sample[1].shape)
	nuar_test,y4 = get_nump(file3,file4)
	logger.debug('测试数据集为:',nuar_test.shape,y4.shape)
	nuar_test = tf.convert_to_tensor(nuar_test, dtype=tf.float32)
	y4_test = tf.convert_to_tensor(y4, dtype=tf.int32)
	# train_db = tf.data.Dataset.from_tensor_slices((nuar,y)).batch(128)
	train_db_test = tf.data.Dataset.from_tensor_slices((nuar_test, y4_test))
	train_db_test = train_db_test.batch(batch)
	logger.debug('train_db_test类型为：',type(train_db_test))
	w1 = tf.Variable(tf.random.truncated_normal([14280, 256], stddev=stddev))
	b1 = tf.Variable(tf.zeros([256]))
	w2 = tf.Variable(tf.random.truncated_normal([256, 128], stddev=stddev))
	b2 = tf.Variable(tf.zeros([128]))
	w3 = tf.Variable(tf.random.truncated_normal([128, 2], stddev=stddev))
	b3 = tf.Variable(tf.zeros([2]))
	lr = 1e-3
	epoch_num = config_h.get_int('mach_lear','epoch_num')

	for epoch in range(epoch_num):
		for step, (x, y) in enumerate(train_db):
			# logger.debug('这个是y:',y)
			x = tf.reshape(x, [-1, 14280])
			with tf.GradientTape() as tape:
				h1 = x @ w1 + tf.broadcast_to(b1, [x.shape[0], 256])
				# h1 = tf.nn.relu(h1)
				h1 = eval(f'tf.nn.{func}(h1)')
				h2 = h1 @ w2 + b2
				h2 = eval(f'tf.nn.{func}(h2)')
				out = h2 @ w3 + b3
				y_onehot = tf.one_hot(y, depth=2)
				loss = tf.square(y_onehot - out)
				loss = tf.reduce_mean(loss)
			grads = tape.gradient(loss, [w1, b1, w2, b2, w3, b3])
			w1.assign_sub(lr * grads[0])
			b1.assign_sub(lr * grads[1])
			w2.assign_sub(lr * grads[2])
			b2.assign_sub(lr * grads[3])
			w3.assign_sub(lr * grads[4])
			b3.assign_sub(lr * grads[5])
			logger.debug(111111,w1.shape)
			logger.debug('b1',b1.shape)
			logger.debug('w2',w2.shape)
			logger.debug('b2',b2.shape)
			logger.debug('w3',w3.shape)
			logger.debug('b3',b3.shape)
			if step % 100 == 0:
				logger.info('%s, %s, loss:, %s' % (epoch, step, float(loss)))
				# pd.DataFrame.to_csv('test.cvs',[w1,b1,w2,b2,w3,b3],)
				# pd.DataFrame.to_csv(w1.value(),mode='a')
		total_correct, total_num = 0, 0
		# logger.info('%s,%s,%s,%s,%s,%s' % (w1,b1,w2,b2,w3,b3))
		for step, (x, y) in enumerate(train_db_test):
			x = tf.reshape(x, [-1, 14280])
			h1 = eval(f'tf.nn.{func}(x@w1 + b1)')
			h2 = eval(f'tf.nn.{func}(h1@w2 + b2)')
			out = h2@w3 + b3
			prob = tf.nn.softmax(out, axis=1)
			pred = tf.argmax(prob,axis=1)
			pred = tf.cast(pred, dtype=tf.int32)
			# logger.debug('这个是pred2：',pred)
			# y: [b]
			# [b], int32
			# logger.debug(pred.dtype, y.dtype)
			correct = tf.cast(tf.equal(pred, y), dtype=tf.int32)
			# logger.debug('这个是y:', y)
			correct = tf.reduce_sum(correct)
			total_correct += int(correct)
			# logger.debug('x.shape[0]:',x.shape[0])
			total_num += x.shape[0]
		total_num = tf.cast(total_num, dtype=tf.int32)
		# logger.debug(total_num)
		# logger.debug(total_correct)
		# logger.debug(type(total_correct),type(total_num))
		acc = total_correct / total_num
		logger.info('test acc: %s' % acc)
		accuracy=config_h.get_float('mach_lear','accuracy')
		if acc > accuracy:
			dir = str((int(time.time())))
			logger.debug(type(w1))
			save_mode(dir, w1,b1, w2, b2, w3, b3)

if __name__ == '__main__':
	data_operation(file1,file2,file_test1,file_test2)
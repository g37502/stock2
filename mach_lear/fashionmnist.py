#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/10/13 
@desc:
'''
# import lib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets,layers, optimizers, Sequential, metrics

import os,sys
import numpy as np
import pandas as pd
# from tools.log_ctrl import logger
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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
	# logger.debug('55555',x1,y1,x2,y2)
	x1 = np.zeros(x1)
	x2 = np.ones(x2)
	nuar = np.vstack((nuar, nuar_limit))
	y = np.hstack((x1, x2))
	return nuar,y
def preprocess(x, y):
	x = tf.cast(x, dtype=tf.float32) / 255
	y = tf.cast(y, dtype=tf.int32)
	return x, y

file1=sys.argv[1]
file2=sys.argv[2]
file3 = sys.argv[3]
file4 = sys.argv[4]
# (x,y),(x_test, y_test) = datasets.fashion_mnist.load_data()

batchsz=128

nuar, y = get_nump(file1, file2)
# logger.debug('学习数据集为：', nuar.shape, y.shape)
nuar = tf.convert_to_tensor(nuar, dtype=tf.float32)
# logger.debug(nuar.shape)
y = tf.convert_to_tensor(y, dtype=tf.int32)
nuar_test, y4 = get_nump(file3, file4)
# logger.debug('测试数据集为:', nuar_test.shape, y4.shape)
nuar_test = tf.convert_to_tensor(nuar_test, dtype=tf.float32)
y4_test = tf.convert_to_tensor(y4, dtype=tf.int32)

db=tf.data.Dataset.from_tensor_slices((nuar,y))
db = db.map(preprocess).shuffle(10000).batch(batchsz)

db_test = tf.data.Dataset.from_tensor_slices((nuar_test,y4_test))
db_test = db_test.map(preprocess).batch(batchsz)



db_iter = iter(db)
sample = next(db_iter)
print('batch:', sample[0].shape, sample[1].shape)

model = Sequential([
	layers.Dense(3600, activation=tf.nn.relu),
	layers.Dense(900, activation=tf.nn.relu),
	layers.Dense(512, activation=tf.nn.relu),
	layers.Dense(256, activation=tf.nn.relu),
	layers.Dense(128, activation=tf.nn.relu),
	layers.Dense(64, activation=tf.nn.relu),
	layers.Dense(32, activation=tf.nn.relu),
	layers.Dense(2, activation=tf.nn.relu),
])

model.build(input_shape=[None,14280])
model.summary()
optimizer = optimizers.Adam(lr=1e-3)

def main():

	for epoch in range(30):
		for step, (x,y) in enumerate(db):
			x = tf.reshape(x, [-1, 14280])
			with tf.GradientTape() as tape:
				logite = model(x)
				y_onehot = tf.one_hot(y, depth=2)
				loss_mse = tf.reduce_mean(tf.losses.MSE(y_onehot, logite))
				loss_ce = tf.losses.categorical_crossentropy(y_onehot, logite, from_logits=True)
				loss_ce = tf.reduce_mean(loss_ce)

			grads = tape.gradient(loss_ce, model.trainable_variables)
			optimizer.apply_gradients((zip(grads, model.trainable_variables)))

			if step % 100 == 0:
				print(epoch, step, 'loss:', float(loss_ce), float(loss_mse))

		total_correct = 0
		total_num = 0
		for x, y in db_test:
			x = tf.reshape(x, [-1, 14280])
			logits = model(x)
			prob = tf.nn.softmax(logits, axis=1)
			pred = tf.argmax(prob, axis=1)
			pred = tf.cast(pred,dtype=tf.int32)
			correct = tf.equal(pred, y)
			correct = tf.reduce_sum(tf.cast(correct,dtype=tf.int32))

			total_correct += int(correct)
			total_num += x.shape[0]

		acc = total_correct / total_num
		print(epoch, 'test acc', acc)

if __name__ == '__main__':
	main()



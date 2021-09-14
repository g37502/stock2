#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/7/13 
@desc:
'''
# import lib
import pymysql
class Mysql_tool(object):
	def __init__(self,user,password,host,db):
		self.db = pymysql.connect(user=user,password=password,host=host,db=db,charset='utf8',
							 ssl={'ssl': {}})
	def operation(self,sql):
		'''sql操作'''
		try:
			self.cursor = self.db.cursor()
			self.res = self.cursor.execute(sql)
			self.db.commit()
			self.cursor.close()
			return self.cursor
		except Exception as e:
			print('operation res:',e)
			self.db.rollback()
			return 1

	def many_insert(self,sql):
		'''多数据入库'''
		try:
			self.cursor = self.cursor()
			self.res = self.cursor.executemany(sql)
			self.db.commit()
			self.cursor.close()
		except Exception as e:
			self.db.rollback()
			print(e)
			return 1
from tools.config import config_h
host=config_h.get_config('Mysql_stock','host')
user=config_h.get_config('Mysql_stock','user')
password=config_h.get_config('Mysql_stock','password')
db=config_h.get_config('Mysql_stock','db')
mysql_19 = Mysql_tool(host=host, user=user, password=password, db=db)
# host_140=config_h.get_config('Mysql_140','host')
# user_140=config_h.get_config('Mysql_140','user')
# password_140=config_h.get_config('Mysql_140','password')
# db_140=config_h.get_config('Mysql_140','db')
# mysql_140 = Mysql_tool(host=host_140, user=user_140, password=password_140, db=db_140)


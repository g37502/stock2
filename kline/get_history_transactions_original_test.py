#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/7/12 
@desc:获取历史交易
'''
# import lib

# from getkline import s
# codes =s.get_identity()

#print(sys.path)
#股票数据从2006年到2021年6月 来做训练数据， 21年7月做测试数据
import pandas as pd
from selenium import webdriver
import datetime
import platform
from tools.log_ctrl import logger
import time

from tools.mysql_tool import mysql_19

from goto import with_goto
from tools.config import config_h


def get_nextday_kday(date,code):
	# date = str(date).split()[0]
	w=datetime.datetime.strptime(date,'%Y-%m-%d').weekday()
	if w == 4:
		date = str(datetime.datetime.strptime(date, '%Y-%m-%d').date() + datetime.timedelta(days=3))
	if w == 5 or w == 6:
		return 0,0
	date = str(datetime.datetime.strptime(date, '%Y-%m-%d').date() + datetime.timedelta(days=1))
	sql = f'select pctChg/100, ceiling(volume/turn)  from kline_kday WHERE   date  = \"{date}\"  and code=\"{code}\"'
	logger.debug(sql)
	res = mysql_19.operation(sql).fetchall()
	logger.debug(res)
	if isinstance(res, int):
		return res
	else:
		if res:
			grow_rate=res[0][0]
			logger.debug(type(grow_rate))
			if grow_rate > 0:
				grow_rate = grow_rate+1

			total_hands = res[0][1]
			return grow_rate,total_hands
		else:
			return 0,0

@with_goto
def get_history_data(date,code):
	logger.debug(code)
	date = str(date).split()[0]
	code = code.replace('.', '')

	details =[]

	if (platform.system() == 'Windows'):
		win_driver_path = config_h.get_config('Path','win_driver_path')
		logger.debug(win_driver_path,111111)
		driver = webdriver.Chrome(win_driver_path)
	elif (platform.system() == 'Linux'):
		linux_driver_path = config_h.get_config('Path','linux_driver_path')
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		log_path=config_h.get_config('Path','driver_path')
		driver = webdriver.Chrome(executable_path=linux_driver_path, chrome_options=chrome_options,
								  service_args=['--verbose', '--log-path=%s' %log_path])
	else:
		logger.warn('未知系统,退出')
		exit()

	for s in range(1,290):
		time.sleep(0.2)
		detail = []
		url = 'http://market.finance.sina.com.cn/transHis.php?symbol=%s&date=%s&page=%s' % (code, date,s)
		logger.debug(url)
		# url = 'https://market.finance.sina.com.cn/transHis.php?symbol=sh600003&date=2006-01-04&page=1'

		try:
			label .begin
			driver.implicitly_wait(3)
			driver.get(url=url)
			try:
				h1 = driver.find_element_by_xpath('//h1')
				if h1:
					if h1.text == '拒绝访问':
						logger.warn('拒绝访问,等待5分钟')
						time.sleep(300)
						goto .begin

			except:
				pass
			html = driver.find_element_by_xpath('//tbody')
			if html.tag_name == 'tbody':
				detail = html.text.replace('\n', ' ').split()
				detail = [detail[i:i + 6] for i in range(0, len(detail), 6)] #将内容每6个做一个列表
				if not detail:
					break
				details.extend(detail)

			else:
				break
		except Exception as e:
			logger.debug(e)

		con = len(detail)
		if con == 0:
			break
	driver.close()
	time.sleep(5)
	return details
def data_arran(data,date,code):
	logger.debug(type(date))
	date = str(date).split()[0]
	df = pd.DataFrame(data)
	df[0] = date + ' ' + df[0]
	df[3] = pd.to_numeric(df[3])
	df=pd.DataFrame(df)
	df[6]=code
	# df.rename(columns={0:'时间',1:'成交价',2:'价格变动',3:'成交量(手)',4:'成交额(元)', 5:'性质',6:'code'},inplace=True)
	df.rename(columns={0:'date',1:'tran_price',2:'price_change',3:'volume',4:'turnover', 5:'nature',6:'code'},inplace=True)
	return df







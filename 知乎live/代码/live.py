#-*-coding:utf-8 -*-
import requests
import urllib2
import urllib
import re
import os
import datetime
import random
import codecs
from lxml import etree
from enum import Enum
import sys
import csv
import inspect
import time
import cookielib
import logging
import json

reload(sys)
sys.setdefaultencoding('utf8');


class zhihulive(object):


	def __init__(self, live_id, save_path):
		
		#初始化所需要的基本参数
		self.default_agetnt = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36';
		self.num_retry = 2;
		
		#初始化传参
		self.live_id 	= live_id;									#全局变量 保存当前live的id	
		self.save_path	= save_path.decode('utf-8');				#全局变量 保存当前live的存储路径

		#初始化日志
		self.Log 		= logging.getLogger("live %d" % live_id);
		formatter 		= logging.Formatter('[%(asctime)s] [%(levelname)-8s]: %(message)s');		#输出日志格式
		
		#日志输出到文件句柄
		file_handler 	= logging.FileHandler("test.log")
		file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

		#日志输出到标准输出的句柄
		console_handler = logging.StreamHandler(sys.stdout)
		console_handler.formatter = formatter  # 也可以直接给formatter赋值

		#添加输出地
		# logger.addHandler(file_handler)
		self.Log.addHandler(console_handler)
		self.Log.setLevel(logging.INFO);

		#初始化完成
		self.Log.info("ZhiHu live %d init success! save path: %s" % (self.live_id, self.save_path.decode('utf-8')));
					


	def curl(self,url, type = None, proxy = None, data = None):
		headers = {
			'User-agent':self.default_agetnt,
			'content-type' :"multipart/form-data; boundary=---------------------------21646385926565",
		};

		request = urllib2.Request(url, data, headers=headers);

		times = self.num_retry;
		while times > 0:
			try:
				html=  urllib2.urlopen(request).read();
				host = urllib2.urlparse.urlparse(url).netloc.split('.');
				break;
			except urllib2.URLError as e:
				self.Log.error("尝试了%s %d 次 失败, 失败原因： %s %s" % (url,self.num_retry - times + 1,'request error:',e) );
				html = None;
				times = times - 1;
		return html;

	def Schedule(self,a,b,c):
		current_bytes = a * b;
		total_bytes   = c;
		# if(a < 1024 * 1024):
		# 	if(current_bytes * 2 > c):
		# 		if("tag" not in locals()):
		# 			print "download 50% +1"
		# 			tag = True;

		# 	elif(current_bytes >= c):
		# 		print "download 100%"

		# elif(a < 10 * 1024 * 1024):

		# 	if(current_bytes * 2 < c):
		# 		print "download 50% +"
		# 	elif(current_bytes >= c):
		# 		print "download 100%"

		# else:
		# 	print "big size"


	def download(self, url, path,count,suffix):

		try:
			urllib.urlretrieve(url,"%s\\%s.%s" % (path,count,suffix),self.Schedule);
			print url, "download to ", path, "success";
		except urllib2.URLError as e:
			self.Log.error("%s download 失败 for %s" % (url,e));


	def login(self, username, passwd):
		print username, passwd;


		self.session = requests.session();
		self.session.cookies = cookielib.LWPCookieJar(filename='cookies');
		try:
			self.session.cookies.load(ignore_discard=True);
		except:
			self.Log.info("cookies 未能正确加载");

		return 1;

	def main(self):
		self.login("username","passwd");



	def test(self):
		# self.Log.debug('this is debug info %s' % 'afds')
		# self.Log.info('this is information')
		# self.Log.warn('this is warning message')
		# self.Log.error('this is error message')
		# self.Log.fatal('this is fatal message, it is zzz顶顶顶 as logger.critical %s %s' % ("adsf","asdfasfd"))
		# self.Log.critical('this is critical message')

		# url = "https://live-audio.vzuu.com/8a48c6a792e6d320aceacb3f1196ffb5";			#其中一条live语音
		# url = "https://api.zhihu.com/lives/776524790524542976/messages?before_id=783076540500959232&chronology=desc&limit=30" #live消息列表
		# url = "https://www.zhihu.com/api/v4/questions/60810304/answers?";				#问题的答案
		# url = "https://zhuanlan.zhihu.com/api/columns/wajuejiprince/followers";		#专栏关注着列表
		# self.download(url,self.save_path,11,"m4a");
		# j = json.loads(self.curl(url));
		# for i in j:
		# 	for k,l in i.items():
		# 		if k=='avatar':
		# 			print l['template'];



		print self.curl("https://api.douban.com/v2/book/2129650");

if __name__ == '__main__':
	live_123 = zhihulive(123, "D:\ZhiHuLive\知乎live\下载");
	live_123.test();
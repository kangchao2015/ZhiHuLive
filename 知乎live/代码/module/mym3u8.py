# coding=utf-8
from selenium import webdriver
import stat
import time
import os
import requests;
import sys;
import json;
import logging;
import datetime;
import urllib;
import urllib2;
import m3u8

reload(sys)
sys.setdefaultencoding('utf-8')


def json_read(path):
	
	try:
		if(os.path.exists(path)):
			pass;
		else:
			return False;

		with open(path, "r") as f:
			str = f.read();
		obj = json.loads(str);
		return obj;

	except Exception as e:
		print e;
		return False;

def download(url,dir,name=None):

    if name == None:
        defaultName = datetime.datetime.now().strftime('%H:%M:%S');
    else:
        defaultName = name;

	try:
		if os.path.exists(dir):
			pass;
		else:
			os.mkdirs(dir);
		path = os.path.join(dir, defaultName); 
		urllib.urlretrieve(url, path);
		return True;
	except Exception as e:
		print "error [%d] " % e.code;
		return False;

url = "http://live-videoreplay.vzuu.com/304a9190vodgzp1253536888/a64219567447398155264771449/playlist.m3u8";
tsurl = "http://live-videoreplay.vzuu.com/304a9190vodgzp1253536888/a64219567447398155264771449/";

def gogogo():
	# S_SESSION	=	requests.Session();	#session
	# cookie 		= 	json_read("../cookie.txt");
	# S_SESSION.cookies.update(self.cookie);


	m3u8obj = m3u8.load(url);
	count = 0;
	for a in m3u8obj.files:
		count += 1;
		print tsurl + a;
		print count;
		if download(tsurl + a,"./ts","%d.ts" % count):
			with opne("./vido.mp4", "a") as f:
				with open("./ts/%d.ts", "r") as p:
					f.write(p);
			


if __name__ == '__main__':
	gogogo();
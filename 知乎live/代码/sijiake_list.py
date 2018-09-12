# coding=utf-8
from selenium import webdriver
import time
import os
import requests;
import sys;
import json;
import logging;
import datetime;
import urllib;
import urllib2;
import ConfigParser
import mysql.connector
import getliveinfo as glive;
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')



ZHIHU_URL 				=	"https://www.zhihu.com"
UESR_NAME 				=	"jushou2018@163.com"
PASSWORD  				=	"20140619fgt"
HEADER	  				=	{'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'};
CHROME_DRIVER_PATH 		=	"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
PHANTOMJS_DRIVER_PATH	=	"C:\\Program Files (x86)\\phantomjs\\phantomjs.exe";
COOKIE_SAVE_PATH		=	"d:\cookie.txt"
VERIFY_CODE_DIR			=	"./Verofy_code/"
LOG_FORMAT				=	"[%(asctime)s] [%(levelname)-7s] - %(message)s"
LOGIN_STATUS			=	False;
TRY_TIMES				=	5;
colums 		= 	[
	["id"],
	["seats","taken"],
	["feedback_score"],
	["fee", "original_price"],
	["starts_at"],
	["outline"],
	["subject"],
	["tags",0,"name"],
	["description"],
	["speaker", "member","name"],
	["speaker", "member","headline"],
	["speaker","description"]
]
#log init
logging.basicConfig(level = logging.INFO,format = LOG_FORMAT);
handler = logging.FileHandler("live_failed.txt")
handler.setLevel(logging.ERROR);
L = logging.getLogger(__name__);
L.addHandler(handler)


def json_save(obj, path):
	if obj == None:
		return False;
	else:
		try:
			str = json.dumps(obj);
			with open(path, "w") as f:
				f.write(str);
			return True;
		except Exception as e:
			print e
			return False;


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

def getElement(driver, xpath):
	try:
		element = driver.find_element_by_xpath(xpath);
		return element;
	except Exception as e:
		return None;

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
		print "error ";
		return False;


def curl(url):

    request = urllib2.Request(url, headers=HEADER);
    times = TRY_TIMES
    while times > 0:

        try:
            html=  urllib2.urlopen(request).read();
            # host = urllib2.urlparse.urlparse(self.url).netloc.split('.');
            break;
        except urllib2.URLError as e:
            if hasattr(e,'code') and  600 > e.code >= 320:
               print "curl error code:%d" % e.code;
            html = None;
            times = times - 1;
    return html;

def db_init():

	try:
		conn = mysql.connector.connect(host='118.190.70.156',user='root', password='root', database='zhihulive', use_unicode=True)
					   # MySQLdb.connect("localhost", "testuser", "test123", "TESTDB", charset='utf8' )
	except Exception as e:
		print e;
		return None;

	cursor = conn.cursor();
	table  = "sijiake_infos".decode("utf-8");
	sql_table_if_exist = "show tables;"
	try:
		cursor.execute(sql_table_if_exist);
	except Exception as e:
		raise e

	tables = cursor.fetchall()
	print tables;
	if (table,) in tables:
		L.info("数据库%s已经存在" % table);
	else:
		L.info("数据库%s已不存在" % table);
		pass;
	cursor.close();
	return conn;

conn = db_init();
if conn == None:
	L.error("数据库链接失败");
	exit();

def dealsijiakeinfo(sijiake_id):
	if sijiake_id == None:
		L.error("sijiake_id not given");
	sijiake_id = int(sijiake_id);
	#check if record exist
	sql = "select * from sijiake_infos where id = '%d'" % int(sijiake_id);
	curson2 = conn.cursor();
	try:
		curson2.execute(sql);
		ret = curson2.fetchall();
		# print len(ret);
		if len(ret) > 0:
			L.info("%d 已经存在 跳过!" % sijiake_id);
			return;
		else:
			pass;
	except Exception as e:
		print e;
		L.error("%d 数据库查询失败" % sijiake_id);
	# curson2.close()

	#####处理具体的live信息
	sijiake_api_url = "https://api.zhihu.com/remix/albums/%d" % int(sijiake_id);
	sijiake_json	 = curl(sijiake_api_url);
	if sijiake_json == None:
		L.error("%d curl获取json失败!" % sijiake_json);
		return;
	else:
		sijiake_obj	 = json.loads(sijiake_json);

	sut_people = "";

	title = sijiake_obj["title"].decode("utf-8");
	for  a in sijiake_obj["suitable_crowd"]:
		sut_people = "%s%s\r\n" % (sut_people, a.decode("utf-8"));
	price 		=  int(sijiake_obj["price"]["origin"]);
	career 		=  sijiake_obj["author"]["career"].decode("utf-8").replace('\'','_')
	bio    		=  sijiake_obj["author"]["bio"].decode("utf-8");
	author 		=  sijiake_obj["author"]["user"]["name"].decode("utf-8");
	keypoint 	=  sijiake_obj["description"]['keypoint'].decode("utf-8");


	#if not exist insert into tabel live_info
	sql = "INSERT INTO `sijiake_infos` ("
	sql += "`id`,`sut_people`,`title`,`price`,`author`,`career`,`keypoint`,`bio`,`accessable`,`episode`) "
	sql += 	"VALUES("
	sql += "%d,'%s','%s',%d,'%s','%s','%s','%s',0,0" % (int(sijiake_id),sut_people,title,int(price),author,career,keypoint,bio)
	sql += ");"

	# cursor1 = conn.cursor();
	try:
		curson2.execute(sql);
	except Exception as e:
		L.error("%d 数据库插入失败" % sijiake_id);
		print sql;
		print e;

	curson2.close();

	# try:
	# 	getliveinfo.doit(sijiake_id,1);
	# except Exception as e:
	# 	L.error("%d live 抓取失败" % sijiake_id);
	L.info("%d end" % sijiake_id);

def get_cat_list():

	length = 10;
	offset = 0;
	count = 0;
	while True:
		info = json.loads(curl("https://api.zhihu.com/remix/albums?limit=%d&offset=%d" % (length, offset) ));
		offset += length;

		for a in info['data']:
			count += 1;
			# dealsijiakeinfo(a["id"]);
			glive.doit(int(a["id"]),6);










		if info["paging"]["is_end"] != False:
			break



	L.warning("所有私家课总计  %d 场" % count);	


# L.error("asdfasdf");
get_cat_list();
conn.commit();
conn.close();
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
import getliveinfo
from lxml import etree
import getliveinfo as glive;

reload(sys) 
sys.setdefaultencoding('utf-8')



ZHIHU_URL 				=	"https://www.zhihu.com"
UESR_NAME 				=	"jushou2018@163.com"
PASSWORD  				=	"20140619fgt"
HEADER	  				=	{'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'};
CHROME_DRIVER_PATH 		=	"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
PHANTOMJS_DRIVER_PATH	=	"C:\\Program Files (x86)\\phantomjs\\phantomjs.exe";
COOKIE_SAVE_PATH		=	"d:\\cookie.txt"
VERIFY_CODE_DIR			=	"./Verofy_code/"
LOG_FORMAT				=	"[%(asctime)s] [%(levelname)-7s] - %(message)s"
LOGIN_STATUS			=	False;
TRY_TIMES				=	5;
# BROWER_CHROME			= 	webdriver.Chrome(CHROME_DRIVER_PATH);
# BROWER_PHANTOMJS		=	webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH);
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


aaaa = [];
txt = "..\\list.txt"
for a in open(txt):
	aaaa.append( int( a.strip().decode("utf-8") ) );


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
	except Exception as e:
		print e;
		return None;

	cursor = conn.cursor();

	sql_table_if_exist = "show tables;"
	try:
		cursor.execute(sql_table_if_exist);
	except Exception as e:
		raise e

	tables = cursor.fetchall()
	if ('live_infos',) in tables:
		L.info("数据库%s已经存在" % "live_infos");
	else:
		L.info("数据库%s已不存在" % "live_infos");
		pass;
		# sql = 	"DROP TABLE IF EXISTS `live_info`;"
		# sql = 	sql +	"CREATE TABLE `live_info` ("
		# sql =   sql +	"`uuid` int(20) NOT NULL AUTO_INCREMENT,"

		# for i in colums:
		# 	c_name = "";
		# 	for j in i:
		# 		c_name = c_name + "_" + str(j);
		# 	c_name = c_name[1:];
		# 	sql = sql + "`%s` varchar(65530) DEFAULT NULL," % c_name;
		  
		# sql =	sql +	"PRIMARY KEY (`uuid`)"
		# sql = 	sql + 	") ENGINE=MyISAM DEFAULT CHARSET=utf8;"
		# print sql;

		# try:
		# 	cursor.execute(sql,multi=True)
		# 	conn.commit();
		# 	L.info("数据库%s创建成功" % "live_info");
		# except Exception as e:
		# 	print e;
	cursor.close();
	return conn;

conn = db_init();

def dealliveinfo(live_id):
	if live_id == None:
		L.error("live_id not given");
	
	#check if record exist
	sql = "select * from live_infos where id = '%d'" % live_id;
	curson2 = conn.cursor();
	try:
		curson2.execute(sql);
		ret = curson2.fetchall();
		# print len(ret);
		if len(ret) > 0:
			L.error("%d 已经存在 跳过!" % live_id);
			return;
		else:
			pass;
	except Exception as e:
		print e;
		L.error("%d 数据库查询失败" % live_id);
	curson2.close()

	#####处理具体的live信息
	live_api_url = "https://api.zhihu.com/lives/%d" % live_id;
	live_json	 = curl(live_api_url);
	if live_json == None:
		L.error("%d curl获取json失败!" % live_id);
		return;
	else:
		live_obj	 = json.loads(live_json);


	colums_info = 	dict();

	for i in colums:
		key = "";
		value = live_obj;
		continue_tag= 0;
		for j in i:
			key = key + "_" + "%s" % j;

			if isinstance(value, dict):
				if value.has_key(j):
					value = value[j];
				else:
					L.error("%d live 没有 %s字段" %(live_id, key[1:]));
					continue_tag = 1;
					break;
			elif isinstance(value, list):
				if len(value) > j:
					value = value[j];
				else:
					L.error("%d live 没有 %s字段" %(live_id, key[1:]));
					continue_tag = 1;
					break;
			else:
				pass;


		if continue_tag == 1:
			continue;
		colums_info[key[1:]] = value;
		

	if conn == None:
		print "conn error"
		return;



	#if not exist insert into tabel live_info
	sql = "INSERT INTO `live_infos` (`uuid`"
	
	for i in colums_info.keys():
		sql = sql + ", `%s`" % i;

	sql = sql + ",`updated_at`) VALUES (null"
	for i,z in colums_info.items():

		if isinstance(z, unicode):
			z = z.replace("\'","_");

		sql = sql +", '%s'" % z;
	sql = sql +	",%d);" % int(time.time());
	print sql;
	return;

	sql = sql.replace('💡','');
	# print sql;
	cursor1 = conn.cursor();
	# print cursor1;
	try:
		cursor1.execute(sql);
	except Exception as e:
		with open("./record/%d.log" % live_id, "w") as f:
			f.write(sql);
		L.error("%d 数据库插入失败" % live_id);
		print e;

	cursor1.close();

	conn.commit();
	# try:
	# 	getliveinfo.doit(live_id,1);
	# except Exception as e:
	# 	L.error("%d live 抓取失败" % live_id);
	L.info("%d end" % live_id);

# dealliveinfo(792363358090326016);


def get_cat_list():
	total_info = "total_info.txt";
	c= json_read(total_info);
	if c == False:
		driver = webdriver.Chrome(CHROME_DRIVER_PATH);
		driver.get("https://www.zhihu.com/market/lives/unlimited/choiceness");
		time.sleep(1);
		a = driver.execute_script("return window.__APP_STATE__");
		time.sleep(2);
		driver.close();
		json_save(a, total_info);
		c = a;
	else:
		pass;


	total_size  = dict();
	statics 	= dict();
	for z in c['prefetch']['LiveUnlimited']['result'][1]['value']:
		b = dict();

		b['name'] 	= z['token'];
		b['count'] 	= z['resource_count'];
		b['c_id'] 	= z['id'];
		total_size[b['c_id']] = b;



	all_total1 				= 0;				#lives count
	all_total2 				= 0;				#lives count
	cat_count 			 	= 0;				#lives category count
	for k,v in total_size.items():
		cat_id 		= int(v['c_id'].encode('utf-8'));
		cat_name 	= v['name'].encode('utf-8');
		cat_count2 	= v['count'];

		# L.info("cat id:%d cat_name:%s cat_count:%d" %(cat_id, cat_name, cat_count));
		all_total1 += cat_count2

		size = 20;				#caount per curl
		offset = 0 ;			#url offset parm
		cat_list_count = 0;
		while True:
			
			
			# catgory_url = 	"https://api.zhihu.com/unlimited/subscriptions/1/resources?limit=%d&offset=%d&tag_id=%d" % (size, offset, cat_id);
			catgory_url = 	"https://api.zhihu.com/lives?limit=%d&offset=%d" % (size, offset);

			target_json = 	curl(catgory_url);
			target_obj	=	json.loads(target_json);	


			cur_cat_count = 0;
			for item in target_obj['data']:
				all_total2			= all_total2 + 1;
				cat_list_count 		= cat_list_count + 1;
				cur_cat_count 		= cur_cat_count + 1;
				live_id = int(item['id'].encode("utf-8"));
				dealliveinfo(live_id);
				# if live_id in aaaa:
				# 	L.info("%d在zip文件夹中" % live_id);
				# else:
				# 	L.info("%d 没有 开始下载" % live_id);
				# 	glive.doit(live_id,1);


			if target_obj['paging']['is_end'] == True:
				break;

			
			offset 	= offset + cur_cat_count;
			# print offset, cat_count,cat_list_count, cur_cat_count,cat_id
		cat_count += 1;
		# L.warning("%12s 类[%d][%2d]的 live 抓取/总计：%d/%d场" % (cat_name,cat_id,cat_offset_cat_count,offset,cat_count));
		

		break;

	L.warning("所有live总计  %d#%d 场" % (all_total1,all_total2));	


# L.error("asdfasdf");
get_cat_list();
conn.close();
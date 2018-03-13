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
from lxml import etree
reload(sys) 
sys.setdefaultencoding('utf-8')



ZHIHU_URL 				=	"https://www.zhihu.com"
UESR_NAME 				=	"17710667921"
PASSWORD  				=	"kc24118242"
HEADER	  				=	{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'};
CHROME_DRIVER_PATH 		=	"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
PHANTOMJS_DRIVER_PATH	=	"C:\\Program Files (x86)\\phantomjs\\phantomjs.exe";
COOKIE_SAVE_PATH		=	"./cookie.txt"
VERIFY_CODE_DIR			=	"./Verofy_code/"
LOG_FORMAT				=	"[%(asctime)s] [%(levelname)-7s] - %(message)s"
LOGIN_STATUS			=	False;
TRY_TIMES				=	2;
# BROWER_CHROME			= 	webdriver.Chrome(CHROME_DRIVER_PATH);
# BROWER_PHANTOMJS		=	webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH);

#log init
logging.basicConfig(level = logging.INFO,format = LOG_FORMAT);
L = logging.getLogger(__name__)


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

    if os.path.exists(dir):
        pass
    else:
        os.mkdir(dir);
    path = os.path.join(dir, defaultName); 

    urllib.urlretrieve(url, path);


def curl(url):

    request = urllib2.Request(url, headers=HEADER);
    times = TRY_TIMES
    while times > 0:

        try:
            html=  urllib2.urlopen(request).read();
            # host = urllib2.urlparse.urlparse(self.url).netloc.split('.');
            break;
        except urllib2.URLError as e:
            L.error(TRY_TIMES,'Download error:',e);
            if hasattr(e,'code') and  600 > e.code >= 320:
                print("lalalal");
            html = None;
            times = times - 1;
    return html;


################  ------------------------------------------------------################################


class zhihulive:

	def __init__(self, live_id, save_path):
		self.live_id 	= 	live_id;			#this is target live id;
		self.save_path 	= 	save_path			#this is target path to save live
		self.s 			=	requests.Session();	#session
		self.cookie 	=	False;				#cookie dick
		self.check_url	=	"https://api.zhihu.com/lives/776524790524542976/messages";	#url to test if login
		self.driver 	=	None;				# explorer driver
		self.confpaser    =	ConfigParser.ConfigParser();
		self.conf_path 	= 	"./config.ini"


		L.info("init success! live_id:[%s] save_path:[%s]" % (self.live_id,self.save_path));


	def checkIfLoginSuccess(self):
		r = self.s.get(self.check_url, headers = HEADER);
		if r.status_code == 200:
			return True;
		else:
			return False;
		pass;

	def go(self):
		step = 0;
		while True:
			step = step + 1;
			step_function = "step%d" % step;
			if(step == 1):
				ret = getattr(self, step_function)();
				if(ret == False):
					# self.driver = webdriver.Chrome(CHROME_DRIVER_PATH);
					pass;
				else:
					# self.driver = webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH);
					
					step = 5;

			else:
				getattr(self, step_function)()

			if(step >= 7):
				break;
			time.sleep(1);

	#cookie load...
	def step1(self):
		L.info("step1 start!");
		self.cookie = json_read(COOKIE_SAVE_PATH);
		if(self.cookie != False):
			L.info("cookies load successfully!");
			self.s.cookies.update(self.cookie);
		else:
			L.info("no cookies file found! start to Login by username and password");
			return False;

		if(self.checkIfLoginSuccess()):
			L.info("cookies status OK! ");
			return True;
		else:
			L.info("cookies experier! start to Login by username and password");
			return False;

	def step2(self):
		L.info("step2 start!");
		self.driver.get(ZHIHU_URL);
		L.info("titile is %s", self.driver.title);

		bt_login = self.driver.find_element_by_xpath("//span[@data-reactid='93']");
		bt_login.click();

	def step3(self):
		L.info("step3 start!");
		input_username = self.driver.find_element_by_xpath("//input[@name='username']");
		input_password = self.driver.find_element_by_xpath("//input[@name='password']");

		input_username.send_keys(UESR_NAME);
		input_password.send_keys(PASSWORD);


	def step4(self):
		L.info("step4 start!");
		bt_submit = self.driver.find_element_by_xpath("//button[@type='submit']");
		verify_code_english = getElement(self.driver, "//img[@class='Captcha-englishImg']");
		verify_code_chinese = getElement(self.driver, "//img[@class='Captcha-chineseImg']");
		if(verify_code_chinese != None or verify_code_english != None):
			if(verify_code_english != None):
				vcode = verify_code_english.get_attribute("src");
			elif(verify_code_chinese != None):
				vcode = verify_code_chinese.get_attribute("src");
			else:
				pass;

			if(vcode == "data:image/jpg;base64,null"):
				L.info("how lucky no verify code!");
			else:
				count = 5;
				while(count > 0):
					time.sleep(1);
					count = count - 1;
					L.info("%ds left to fill in the verify code befor login" % count);

		bt_submit.click();

		if(self.checkIfLoginSuccess):
			L.info("Login successfully!");
		else:
			L.error("Login failed!");

	def step5(self):
		L.info("step5 start!");
		self.cookie = dict();
		for item in self.driver.get_cookies():
			self.cookie[item['name']] = item['value'];

		self.s.cookies.update(self.cookie);
		if(self.checkIfLoginSuccess):
			L.info("cookies update successfully");
			if(json_save(self.cookie,COOKIE_SAVE_PATH)):
				L.info("cookies saved successfully!");
			else:
				L.info("cookies saved failed!");

		else:
			L.error("cookies update failed!");


	def step6(self):
		L.info("step6 start!");

		live_url 		= "https://www.zhihu.com/lives/%d" % self.live_id;

		title 	= "";
		score 	= "";
		author 	= "";

		if(not os.path.exists("./record/%d.conf" % self.live_id)):

			L.info(live_url);

			self.driver = webdriver.Chrome(CHROME_DRIVER_PATH);
			self.driver.get(live_url);
			L.info("等待页面加载... 7s");
			time.sleep(7);
			entrance_html	= self.driver.page_source;
			# print entrance_html;
			if(entrance_html != None):
				potral_page = etree.HTML(entrance_html.decode('utf-8'));
				L.info("portal page get successfully!");
			else:	
				L.error("can't get the html of the entrance URL!");

			node_title 	= potral_page.xpath("//div[@class='LivePageHeader-line-SzR2 LivePageHeader-title-1RQL']");	
			node_score 	= potral_page.xpath("//span[@class='LiveContentInfo-scoreNum-Qa-K']");
			node_author = potral_page.xpath("//a[@class='LiveSpeakers-link-6dN8 UserLink-root-1ogW']");

			if(len(node_title) ==  1):
				title = node_title[0].text;
			else:
				title = "NO TITILE GET!"

			if(len(node_score) ==  1):
				score = node_score[0].text;
			else:
				score = "NO TITILE GET!"

			if(len(node_author) ==  1):
				author = node_author[0].text;
			else:
				author = "NO AUTHOR GET!"


			self.driver.close();

			if os.path.exists("./record/"):
				pass;
			else:
				os.makedirs("./record/");

			self.confpaser.add_section('config')
			self.confpaser.set('config',"title",title);
			self.confpaser.set('config',"score",score);
			self.confpaser.set('config',"id",self.live_id);
			self.confpaser.write(open("./record/%d.conf" % self.live_id,"w"));
		else:
			L.info("当前live的配置信息存在 读取配置文件... ./record/%d.conf" % self.live_id);
			self.confpaser.read("./record/%d.conf" % self.live_id);
			title = self.confpaser.get("config", "title").decode('utf-8');
			score = self.confpaser.get("config", "score");

		# live_dir_name 	= "%s_%s_%s_%d" % (title, score,author, self.live_id)
		live_dir_name 	= "%s_%s_%d" % (title, score, self.live_id)
		target_dir 		= os.path.join(self.save_path, live_dir_name);

		if os.path.exists(target_dir):
			L.info("目录[%s]已经存在！" % (target_dir));
		else:
			os.makedirs(target_dir);
			L.info("目录[%s]创建成功！" % (target_dir));	

		L.info("当前正在抓取的live:《%s》,评分：[%s],id:[%d], 作者:%s" % (title, score,self.live_id, author));


	def step7(self):
		L.info("step7 started");
		way_go 		= "chronology";
		limit 		= "limit";
		after_id 	= "after_id"



		total_api	= "https://api.zhihu.com/lives/%d/messages?chronology=asc&limit=1" % self.live_id;

		total_api	= "https://api.zhihu.com/lives/%d/messages?chronology=asc&limit=1" % self.live_id;
		r = self.s.get(total_api, headers = HEADER);
		if r.status_code == 200:
			data_json_text 	= 	r.text;
			data_obj		=	json.loads(data_json_text);
			for k,v in data_obj.items():
				if k == "unload_count":
					total_count = int(v);
					L.info("live:%d 总计条数:%d" % (self.live_id, total_count));
				elif k == "data":
					for item in data_obj['data']:
						first_id = int(item['id'].encode('utf-8'));
						L.info("live:%d 的第一条记录id:%d" % (self.live_id, first_id));
				else:
					continue;
		else:
			L.error("抓取live总条数失败！live id :%d" % self.live_id);

		item_count_done = 0;
		is_first_curl = True

		last_item_id = 0;
		while item_count_done < total_count:
			# L.info("last item id %d" % last_item_id);
			if is_first_curl:
				target_api = "https://api.zhihu.com/lives/%d/messages?chronology=asc&limit=30" % (self.live_id);
			else:
				target_api = "https://api.zhihu.com/lives/%d/messages?after_id=%d&chronology=asc&limit=30" % (self.live_id, last_item_id);
			
			r = self.s.get(target_api, headers = HEADER);
			if r.status_code == 200:
				is_first_curl = False;
				count = 0;
				data_json_text 	= 	r.text;
				data_obj		=	json.loads(data_json_text);
				for k,v in data_obj.items():
					if k == "data":
						for item in data_obj['data']:

							last_item_id = int(item['id'].encode('utf-8'));
							count = count + 1;
					elif k == "unload_count" :
						unload_count = v;
					else:
						# print "%s ==> %s" %(k,v);
						pass;
				L.info("本次总共抓取条数：%d 总计抓取条数：%d api 剩余套数：%d 计算剩余条数:%d" % (count,item_count_done,unload_count,total_count-item_count_done));
			else:
				L.error("目标抓取失败！live id :%d" % self.live_id);

			item_count_done = item_count_done + count;



a = zhihulive(776524790524542976, "../download/");
a.go();

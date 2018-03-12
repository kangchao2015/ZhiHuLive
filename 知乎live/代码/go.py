from selenium import webdriver
import time
import os
import requests;
import sys;
import json;
import logging;

ZHIHU_URL 				=	"https://www.zhihu.com"
UESR_NAME 				=	"17710667921"
PASSWORD  				=	"kc24118242"
HEADER	  				=	{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'};
CHROME_DRIVER_PATH 		=	"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
PHANTOMJS_DRIVER_PATH	=	"C:\\Program Files (x86)\\phantomjs\\phantomjs.exe";
COOKIE_SAVE_PATH		=	"./cookie.txt"
LOG_FORMAT				=	"[%(asctime)s] [%(levelname)-7s] - %(message)s"
LOGIN_STATUS			=	False;
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

class zhihulive:

	def __init__(self, live_id, save_path):
		self.live_id 	= 	live_id;			#this is target live id;
		self.save_path 	= 	save_path			#this is target path to save live
		self.s 			=	requests.Session();	#session
		self.cookie 	=	False;				#cookie dick
		self.check_url	=	"https://api.zhihu.com/lives/776524790524542976/messages";	#url to test if login
		self.driver 	=	None;				# explorer driver


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
					self.driver = webdriver.Chrome(CHROME_DRIVER_PATH);
				else:
					self.driver = webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH);
					step = 5;

			else:
				getattr(self, step_function)()

			if(step >= 5):
				break;
			time.sleep(1);

	#cookie load...
	def step1(self):
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
		self.driver.get(ZHIHU_URL);
		L.info("titile is %s", self.driver.title);

		bt_login = self.driver.find_element_by_xpath("//span[@data-reactid='93']");
		bt_login.click();

	def step3(self):
		input_username = self.driver.find_element_by_xpath("//input[@name='username']");
		input_password = self.driver.find_element_by_xpath("//input[@name='password']");

		input_username.send_keys(UESR_NAME);
		input_password.send_keys(PASSWORD);


	def step4(self):
		bt_submit = self.driver.find_element_by_xpath("//button[@type='submit']");
		bt_submit.click();
		verify_code_english = getElement(self.driver, "//img[@class='Captcha-englishImg']");
		verify_code_chinese = getElement(self.driver, "//img[@class='Captcha-chineseImg']");
		if(verify_code_chinese != None or verify_code_english != None):
			if(verify_code_english != None):
				print verify_code_english.get_attribute("src");
			elif(verify_code_chinese != None):
				print verify_code_chinese.get_attribute("src");
			else:
				pass;
			time.sleep(5);



	def step5(self):
		print "step555";






a = zhihulive(748872049438490624, "../download/");
a.go();

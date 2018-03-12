from selenium import webdriver
import time
import os
import requests;
import sys;
import json;
import logging

cookie_path = "./cookie.txt";

logging.basicConfig(level = logging.INFO,format = '[%(asctime)s]  [%(levelname)-7s] - %(message)s')
logger = logging.getLogger(__name__)

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

#####		function exit above      #######

chrome_driver_path 		= "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
phantomjs_driver_path	= "C:\\Program Files (x86)\\phantomjs\\phantomjs.exe";
url_live = "https://api.zhihu.com/lives/776524790524542976/messages?before_id=783076540500959232&chronology=desc&limit=3" 
os.environ["webdriver.chrome.driver"] = chrome_driver_path
# browser = webdriver.PhantomJS(phantomjs_driver_path);
browser = webdriver.Chrome(chrome_driver_path);
headers =  {  
        'User-Agent': r'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT) '  
                    r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3'
        }  

# username = "13520892080"
# password = "20140619fgt"
username = "17710667921"
password = "kc24118242"

url = "https://www.zhihu.com" 
status = False;

s = requests.Session();
cookies = json_read(cookie_path);

browser.get(url)
if cookies == False:
	print "no cookies to load";

	#step1
	print browser.title;

	bt_login = browser.find_element_by_xpath("//span[@data-reactid='93']");
	bt_login.click();

	#step3
	input_username = browser.find_element_by_xpath("//input[@name='username']");
	input_password = browser.find_element_by_xpath("//input[@name='password']");

	input_username.send_keys(username);
	input_password.send_keys(password);

	#step 4
	bt_submit = browser.find_element_by_xpath("//button[@type='submit']");

	time.sleep(5);
	bt_submit.click();
	time.sleep(5);
	while True:

		verify_code_english = getElement(browser, "/img[@class='Captcha-englishImg");
		verify_code_chinese = getElement(browser, "/img[@class='Captcha-chineseImg");

		print verify_code_chinese;
		print verify_code_english;

		if verify_code_chinese != None  or verify_code_english !=None:
			if verify_code_english != None:
				print verify_code_english.get_attribute("src");
			else:
				pass;

			if verify_code_chinese !=  None:
				verify_code_chinese.get_attribute("src");
			else:
				pass;

			print "please input chinese code"
			time.sleep(5);
		else:
			break;



	#step 5 
	cookies = dict();  
	for item in browser.get_cookies():
		cookies[item['name']] = item['value'];
	s.cookies.update(cookies);

	r = s.get(url_live, headers = headers);
	if r.status_code == 200:
		logger.info("login success!");
		if json_save(cookies,cookie_path) == True:
			logger.info("cookies saved successfuly!");
			status = True;
	else:
		logger.info("login faile didn't save cookies %d" % r.status_code);
		status = False;
		try:
			os.remove(cookie_path);
		except Exception as e:
			pass;

else:
	logger.info("cookies load success from %s " % cookie_path);
	s.cookies.update(cookies);
	status = True


if status:
	r = s.get(url_live, headers = headers);
	# print r.text;
	if r.status_code == 200:
		count = 0;
		a = json.loads(r.text);
		for z in a['data']:
			count = count +1 ;
			print z;
			print "---------"
		print logger.info("read %d items" %  count);

	else:
		print "failed to get content %d " % r.status_code;
else:
	pass;


# browser.quit()
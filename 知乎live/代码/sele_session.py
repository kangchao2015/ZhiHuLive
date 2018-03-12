from selenium import webdriver
import time
import os
import requests;
import sys;

chrome_driver_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
url_live = "https://api.zhihu.com/lives/776524790524542976/messages?before_id=783074671179354112&chronology=desc&limit=3" 
os.environ["webdriver.chrome.driver"] = chrome_driver_path
browser = webdriver.Chrome(chrome_driver_path);
headers =  { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }  
username = "17710667921"
password = "kc24118242"

url = "https://www.zhihu.com" 



def getElement(driver, xpath):
	try:
		element = driver.find_element_by_xpath(xpath);
		return element;
	except Exception as e:
		return None;



browser.get(url);
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

bt_submit.click();
time.sleep(5);

#step 5 
cookies = dict();  
for item in browser.get_cookies():
	cookies[item['name']] = item['value'];

s = requests.Session();
s.cookies.update(cookies);
r = s.get(url_live, headers = headers);


print r.status_code;
print r.text;
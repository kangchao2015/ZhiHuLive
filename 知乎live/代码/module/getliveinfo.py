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
from pydub import AudioSegment

reload(sys)
sys.setdefaultencoding('utf-8')
	#audio file init

ZHIHU_URL				=	"https://www.zhihu.com"
UESR_NAME 				=	"jushou2018@163.com";
PASSWORD  				=	"20140619fgt";
HEADER	  				=	{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'};
CHROME_DRIVER_PATH 		=	"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe";
PHANTOMJS_DRIVER_PATH	=	"C:\\Program Files (x86)\\phantomjs\\phantomjs.exe";
COOKIE_SAVE_PATH		=	"./cookie.txt"
VERIFY_CODE_DIR			=	"./Verofy_code/"
LOG_FORMAT				=	"[%(asctime)s] [%(levelname)-7s] - %(message)s"
LOGIN_STATUS			=	False;
TRY_TIMES				=	2;

logging.basicConfig(level = logging.INFO,format = LOG_FORMAT);
handler = logging.FileHandler("log.txt")
L = logging.getLogger(__name__);
L.addHandler(handler);



def audio_init(file):
	return AudioSegment.from_file(file);


#make file2 append to audio1
def audio_append(audio1, file2):
	a2 = AudioSegment.from_file(file2);
	return audio1.append(a2);

#audio file export to specific formt file
def audio_export(audio, path, file, format):
	file = os.path.join(path, "%s.%s" % (file, format) );
	audio.export(file, format=format);
	L.info("export to %s" % file);


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
            L.error(TRY_TIMES,'Download error:',e);
            if hasattr(e,'code') and  600 > e.code >= 320:
               print "curl error code:%d" % e.code;
            html = e.code;
            times = times - 1;
    return html;




def configinit(username, password):
	pass;


	######################## -_- -_- -_- -_- -_- -_- -_- -_- -_- -_- -_- -_- ################################


class zhihulive:

	def __init__(self, live_id, save_path):
		self.live_id 	= 	live_id;			#this is target live id;
		self.save_path 	= 	save_path			#this is target path to save live
		self.target_dir = 	""
		self.s 			=	requests.Session();	#session
		self.cookie 	=	False;				#cookie dick
		self.check_url	=	"https://api.zhihu.com/lives/776524790524542976/messages";	#url to test if login
		self.driver 	=	None;				# explorer driver
		self.confpaser  =	ConfigParser.ConfigParser();
		self.conf_path 	= 	"./config.ini"
		self.audio_count=	0;
		self.audio_file =	0;

		self.author 	=	""
		self.score 		=	0;
		self.titile		=	"";


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
			elif(step == 6):
				if(getattr(self, step_function)()):
					pass;
				else:
					L.error("live:%d抓取失败！" % self.live_id);
					return; 
			else:
				getattr(self, step_function)()

			if(step >= 7):
				break;
			time.sleep(1);

	#cookie load...
	def step1(self):
		L.debug("step1 start!");
		self.cookie = json_read(COOKIE_SAVE_PATH);
		if(self.cookie != False):
			L.debug("cookies load successfully!");
			self.s.cookies.update(self.cookie);
		else:
			L.warning("no cookies file found! start to Login by username and password");
			return False;

		if(self.checkIfLoginSuccess()):
			L.debug("cookies status OK! ");
			return True;
		else:
			L.warning("cookies experier! start to Login by username and password");
			return False;

	def step2(self):
		L.debug("step2 start!");
		self.driver = webdriver.Chrome(CHROME_DRIVER_PATH);
		# self.driver = webdriver.PhantomJS(PHANTOMJS_DRIVER_PATH);
		self.driver.get(ZHIHU_URL);
		L.debug("titile is %s", self.driver.title);

		bt_login = self.driver.find_element_by_xpath("//span[@data-reactid='93']");
		bt_login.click();

	def step3(self):
		L.debug("step3 start!");
		input_username = self.driver.find_element_by_xpath("//input[@name='username']");
		input_password = self.driver.find_element_by_xpath("//input[@name='password']");

		input_username.send_keys(UESR_NAME);
		input_password.send_keys(PASSWORD);


	def step4(self):
		L.debug("step4 start!");
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
		L.debug("step5 start!");
		self.cookie = dict();
		for item in self.driver.get_cookies():
			self.cookie[item['name']] = item['value'];

		self.s.cookies.update(self.cookie);
		if(self.checkIfLoginSuccess):
			L.info("cookies update successfully");
			if(json_save(self.cookie,COOKIE_SAVE_PATH)):
				L.info("cookies saved successfully!");
				self.driver.close();
			else:
				L.info("cookies saved failed!");

		else:
			L.error("cookies update failed!");


	def step6(self):
		L.debug("step6 start!");

		live_url 		= "https://www.zhihu.com/lives/%d" % self.live_id;
		if(not os.path.exists("./record/%d.conf" % self.live_id)):

			live_api_url = "https://api.zhihu.com/lives/%d" % self.live_id;
			live_json	 = curl(live_api_url);
			if live_json == None:
				L.error("%d curl获取json失败!" % live_id);
				return;
			else:
				live_obj	 = json.loads(live_json);

			self.author = live_obj['speaker']['member']['name'];
			self.score = live_obj['feedback_score'];
			self.title = live_obj['subject']


			if os.path.exists("./record/"):
				pass;
			else:
				os.makedirs("./record/");

			self.confpaser.add_section('config')
			self.confpaser.set('config',"title",self.title);
			self.confpaser.set('config',"author",self.author);
			self.confpaser.set('config',"score",self.score);
			self.confpaser.set('config',"id",self.live_id);
			self.confpaser.write(open("./record/%d.conf" % self.live_id,"w"));
			L.debug("配置文件写入成功！./record/%d.conf" % self.live_id);
		else:
			L.debug("当前live的配置信息存在 读取配置文件... ./record/%d.conf" % self.live_id);
			self.confpaser.read("./record/%d.conf" % self.live_id);
			self.title = self.confpaser.get("config", "title").decode('utf-8');
			self.author = self.confpaser.get("config", "author").decode('utf-8');
			self.score = self.confpaser.get("config", "score");


		# live_dir_name 	= "%s_%s_%s_%d" % (title, score,author, self.live_id)
		live_dir_name 	= "%s_%s_%d" % (self.title, self.score, self.live_id)
		self.target_dir 		= os.path.join(self.save_path, live_dir_name);

		if os.path.exists(self.target_dir ):
			L.debug("目录[%s]已经存在！" % (self.target_dir ));
		else:
			try:
				os.makedirs(self.target_dir );
				L.debug("目录[%s]创建成功！" % (self.target_dir ));	
			except Exception as e:
				L.error("目录[%s]创建失败！" % (self.target_dir ));
				return False;

		L.debug("当前正在抓取的live:《%s》,评分：[%s],id:[%d], 作者:%s" % (self.title, self.score,self.live_id, self.author));
		return True;

	def step7(self):
		L.debug("step7 started");
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
					L.debug("live:%d 总计条数:%d" % (self.live_id, total_count));
				elif k == "data":
					for item in data_obj['data']:
						first_id = int(item['id'].encode('utf-8'));
						L.debug("live:%d 的第一条记录id:%d" % (self.live_id, first_id));
				else:
					continue;
		else:
			if r.status_code == 403:
				L.warning("您没有权限收听《%s》" % self.title);
			else:
				L.error("抓取live总条数失败！live id :%d 状态码：%d" % (self.live_id, r.status_code));
			return False;	

		item_count_done = 0;
		is_first_curl = True
		
		L.warning("开始抓取：%d" % self.live_id);
		
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
				# print r.text;
				data_obj		=	json.loads(data_json_text);

				for k,v in data_obj.items():
					if k == "data":
						for item in data_obj['data']:

							item_count_done = item_count_done +1;
							item_id 		= int(item['id'].encode('utf-8'));
							role 			= item["sender"]["role"];

							local_dir = os.path.join(self.target_dir, "%d_%d_%s" % (item_count_done, item_id, role)) ;
							if os.path.exists(local_dir):
								pass;
							else:
								os.makedirs(local_dir);
							
							if item.has_key('type'):
								ty = item['type'];

								# print ty;
								if ty == "text":
									if item.has_key('text'):
										text_name = "%s.txt" % item_id;
										text_path = os.path.join(local_dir, text_name);
										if not os.path.exists(text_path):
											with open(text_path,"w") as f:
												f.write("%s" % item['text']);
											L.debug("[+++][text]%d - %d 保存成功" % (item_count_done, item_id));
										else:
											L.debug("[---][text]%d - %d文本信息 已经存在 跳过" % (item_count_done, item_id));
									else:
										L.error("%d - %d 没有text信息" % (item_count_done, item_id));
								elif ty == "audio":

									if item.has_key('audio') and item['audio'].has_key('url'):
										audio_url = item['audio']['url'];
										# local_local_path = os.path.join(local_dir, "%d.m4a" % item_id);
										audio_name = "%d.m4a" % item_id
										audio_full_name = os.path.join(local_dir, audio_name);
										if not os.path.exists(audio_full_name):
											if download(audio_url, local_dir, audio_name) == True:
												L.debug("[+++][audio] %d download successfully count :%d" % (item_id,item_count_done));
											else:
												L.error("[xxx][audio]download failed %d" % item_id);
										else:
											L.debug("[---][audio]%s 已经存在 跳过" % audio_name);
									else:
										pass;

									self.audio_count += 1;
									L.debug(self.audio_count);
									if self.audio_count == 1:
										self.audio = audio_init(audio_full_name);
									elif self.audio_count % 30 == 0:
										self.audio = audio_append(self.audio, audio_full_name);

										audio_export(self.audio, self.target_dir , "%s_%s_%d_%d" % (self.title, self.author ,self.audio_file, self.audio_count) , "wav")
										self.audio_file += 1;
										self.audio_count = 0;
									else:
										self.audio = audio_append(self.audio, audio_full_name);
								elif ty == "image":
									if item.has_key('image') and item['image'].has_key('full'):
										image_url 	= 	item['image']['full']['url'];
										image_name 	=	"%d.jpg" % item_id; 
										if not os.path.exists(os.path.join(local_dir, image_name)):
											if download(image_url, local_dir, image_name) == True:
												L.debug("[+++][image] %d download successfully count :%d" % (item_id,item_count_done));
											else:
												L.error("[xxx][image]download failed %s" % image_url);
										else:
											L.debug("[---][image]%s 已经存在 跳过" % image_url);
									else:
										pass;
								elif ty == "multiimage":
									if item.has_key("multiimage"):
										pos = 0;
										for pic in item["multiimage"]:
											pos += 1;
											pic_name	=	"%d.jpg" % pos; 
											pic_url 	=	pic["full"]["url"];
											if not os.path.exists(os.path.join(local_dir, pic_name)):
												if download(pic_url, local_dir, pic_name) == True:
													L.debug("[+++][mpic] %d download successfully count :%d--%d" % (item_id,item_count_done, pos));
												else:
													L.error("[xxx][mpic]download failed %s" % pic_url);
											else:
												L.debug("[---][mpic]%s 已经存在 跳过" % pic_url);

									else:
										pass;
								elif ty == "video":
									if item.has_key("video") and item["video"].has_key("playlist"):
										pos = 0;
										for vd in item["video"]["playlist"]:
											pos += 1;
											video_name = "%d.mp4" % pos;
											video_url  = vd["url"];
											if not os.path.exists(os.path.join(local_dir, video_name)):
												if download(video_url, local_dir, video_name) == True:
													L.debug("[+++][video] %d download successfully count :%d--%d" % (item_id,item_count_done, pos));
												else:
													L.error("[xxx][video]download failed %s" % image_url);
											else:
												L.debug("[---][video]%s 已经存在 跳过" % image_url);
									else:
										pass;
								elif ty == "reward":
									pass;
								elif ty == "file":
									if item.has_key('file') and item['file'].has_key('url'):
										file_url 	= 	item['file']['url'];
										file_name 	=	item['file']['file_name'];
										if not os.path.exists(os.path.join(local_dir, file_name)):
											if download(file_url, local_dir, file_name) == True:
												L.debug("[+++][file] %d download successfully count :%d" % (item_id,item_count_done));
											else:
												L.error("[xxx][file]download failed %s" % image_url);
										else:
											L.debug("[---][file]%s 已经存在 跳过" % image_url);
										L.debug(item_count_done);
									else:
										pass;
								else:
									L.error("item id:%d 为未知类型消息 type:%s" % (item_id,ty));
							else:
								L.error("%d 没有type字段 无法判断消息类型！" % item_id);

							if item.has_key("sender") and item['sender'].has_key("member"):
								xname 	= item['sender']['member']['name'];
								xdesc	= item['sender']['member']['headline'];

								author_name = "author_type.txt";
								author_path =  os.path.join(local_dir,author_name);
								if not os.path.exists(author_path):
									with open(author_path,"w") as f:
										f.write("%s - %s [%s]" % (xname, xdesc, ty));
									L.debug("[+++][author]%d - %d 作者信息 保存成功" % (item_count_done, item_id));
								else:
									L.debug("[---][author]%d - %d作者信息 已经存在 跳过" % (item_count_done, item_id));
							else:
								L.error("[xxx][author]%d - %d作者信息 不存在" % (item_count_done, item_id));

							last_item_id = int(item['id'].encode('utf-8'));
							count = count + 1;
					elif k == "unload_count" :
						unload_count = v;
					else:
						# print "%s ==> %s" %(k,v);
						pass;
				L.debug("本次总共抓取条数：%-2d 总计抓取条数：%-4d 当前抓取之前的剩余条数(API)：%-4d 剩余抓取:%d" % (count,item_count_done,unload_count,total_count-item_count_done));
			else:
				L.error("目标抓取失败！live id :%d" % self.live_id);
			L.warning("抓取《%s》抓取%d/%d ".encode("utf-8") % (self.title, item_count_done, total_count));
		audio_export(self.audio, self.target_dir , "%s_%s_%d_%d" % (self.title, self.author,self.audio_file, self.audio_count) , "wav")


def doit(liveids):
	if isinstance(liveids, long):
		a = zhihulive(liveids, "../download");
		a.go();
	elif isinstance(liveids, list):
		current = 0;
		total 	=	len(liveids);
		for a in liveids:
			current += 1;
			L.info("共要抓取%d个live, 当前正要抓取第 %d/%d个" % (total,current,total));
			b = zhihulive(a, "../download");
			b.go();
			L.info("当前正要抓取第 %d/%d个 操作完成" % (current,total));
	else:
		L.error("未知ID类型");


if __name__ == '__main__':
	pass;
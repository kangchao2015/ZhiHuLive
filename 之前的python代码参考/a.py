#-*-coding:utf-8 -*-
#-*-coding:utf-8 -*-

#from download import *
import urllib2
import urllib
import re
import os
import datetime
import random
import codecs
from lxml import etree
import sys
import csv
import inspect
reload(sys)
sys.setdefaultencoding('utf8');




class douban(object):
	def __init__(self, douban_id, path):
		self.url = ""
		self.num = 2;
		self.default_agetnt = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36';
		self.default_agetnt1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
		self.path = path;
		self.target_path = "";

		self.result = {};
		self.col = {'性别':'info_sex','星座':'info_mark','出生日期':'info_birthday','出生地':'info_birthplace','职业':'info_job'};
		self.totalimg = ''
		self.num_retry = 2;

		self.imgqueue 	= set([]);
		self.imglist  	= set([]);
		self.actorset 	= set([]);
		self.actorlist	= set([]);

		self.count = 1;

		self.url = "https://movie.douban.com/celebrity/%d" %  douban_id;

		# self.actor_loop();
		ret = self.main();
		if ret != None:
			print self.totalimg 
			self.getimageurllist(self.result['info_imageurl']);
	
	def actor_loop(self):
		if self.url not in self.actorset:
			ret = self.main();
			if ret != None:
				print self.totalimg 
				self.getimageurllist(self.result['info_imageurl']);
			self.actorset.add(self.url);

		portal_html = self.curl("%s%s" % (self.url, 'partners'));
		if portal_html == None:
			print "curl error"
			return None;
		else:
			potral_page = etree.HTML(portal_html.decode('utf-8'));

		actors_node = potral_page.xpath("//div[@class='partners item']");
		for act  in actors_node:
			act_url = act.xpath("./div[@class='pic']/a");
			if len(act_url) > 0:
				url = act_url[0].attrib['href'];
				print url

		page_node = potral_page.xpath("//div[@class='paginator']");
		for page  in page_node[0].xpath(".//a"):
			page_url = page.attrib['href'];
			print urllib2.urlparse.urljoin(self.url,'partners', page_url); 


	def list_loop(self,url):
		try:
			if url not in self.actorlist:
				portal_html = self.curl(url);
				if portal_html == None:
					print "curl error"
					return None;
				else:
					potral_page = etree.HTML(portal_html.decode('utf-8'));
				self.actorlist.add(url);
			else:
				return ;

			actors_node = potral_page.xpath("//div[@class='partners item']");
			for act  in actors_node:
				act_url = act.xpath("./div[@class='pic']/a");
				if len(act_url) > 0:
					url = act_url[0].attrib['href'];
					self.list_loop(urllib2.urlparse.urljoin(url,'partners'));
					self.url = url;
					ret = self.main();
					if ret != None:
						print self.totalimg 
						self.getimageurllist(self.result['info_imageurl']);

			page_node = potral_page.xpath("//div[@class='paginator']");
			if len(page_node) > 0:
				for page  in page_node[0].xpath(".//a"):
					page_url = page.attrib['href'];
					self.list_loop(urllib2.urlparse.urljoin(page_url,'partners'));
		except Exception as e:
			print "list_loop %s" % e;
	
	def get_images(self,url):
		image_html = self.curl(url);
		try:
			image_html_portal = etree.HTML(image_html.decode('utf-8'));
			url = image_html_portal.xpath("//div[@class='photo-show']")[0].xpath(".//img")[0];
			tail = url.attrib['src'].split('.');
			self.download(url.attrib['src'],self.target_path, "%d.%s" % (self.count, tail[-1]) );
			print url.attrib['src'], self.count,"/",self.totalimg,"------",self.result['info_name'];
	#		print tail
		except Exception as e:
			print "image download fail %d" % self.count;


	def getimageurllist(self,url):
		try:
			if url not in self.imglist:
				image_html = self.curl(url);
				self.imglist.add(url);
			else:
				return;

			potral_page = etree.HTML(image_html.decode('utf-8'));
			zzz = potral_page.xpath("//ul[@class='poster-col3 clearfix']")[0];
			for z in zzz:
				image_url = z.xpath('.//a')[0].attrib['href'];
				if image_url not in self.imgqueue:
					self.get_images(image_url);
					self.imgqueue.add(image_url);
					self.count = self.count + 1;

			lll = potral_page.xpath("//div[@class='paginator']")[0];
			for l in lll.xpath(".//a"):
				link = l.attrib['href'];
				self.getimageurllist(link);
				self.imglist.add(link);

		except Exception as e:
			print "getimageurllist %s" % e;

	def show_info(self):
		for i, j in self.result.items():
			print  "%10s" % j,
		print '';

	def get_all_link(self,html):
	    link_reg = '<a[^>]+href=["\'](.*?)["\']' 
	    reg_obj = re.compile(link_reg, re.IGNORECASE);
	    return reg_obj.findall(html);

	def main(self):

		#初始化
		if os.path.exists(self.path):
			pass
		else:
			os.makedirs(self.path);
		self.result = {};
		self.count = 1;
		self.imgqueue 	= set([]);
		self.imglist  	= set([]);

		#抓取页面
		portal_html  = self.curl(self.url);
		if portal_html == None:
			print "curl error"
			return None;
		else:
			potral_page = etree.HTML(portal_html.decode('utf-8'));

		#获取相册入口url self.info_imageurl
		portal_image_node = potral_page.xpath("//div[@id='photos']");
		if(len(portal_image_node)  != 1):
			print "don't have portal_image_node";
		portal_image_node = portal_image_node[0];
		
		portal_img_node_1 = portal_image_node.xpath(".//a");

		if portal_img_node_1[0] is not None:
			self.result['info_imageurl'] = portal_img_node_1[0].attrib['href'];
			self.totalimg = portal_img_node_1[0].text;

		#获取其他信息
		portal_info_node = potral_page.xpath("//div[@id='content']");
		portal_name_node = portal_info_node[0].xpath(".//h1");
		if len(portal_info_node) !=  1:
			print "don't have name portal_name_node"
		portal_name_node = portal_name_node[0]
		self.result['info_name'] = portal_name_node.text;

		portal_other_node = portal_info_node[0].xpath(".//div[@class='info']/ul")[0].getchildren();
		for z in self.col:
			for i in portal_other_node:	
				if z == i.xpath("span")[0].text:
						self.result[self.col[z]] = i.xpath("span")[0].tail.strip(':').strip();

		if 'info_sex' in self.result and self.result['info_sex'] != '女':
			pass;

		if 'info_job' in self.result and self.result['info_job'][0:2] != '演员':
			pass;
		

		self.target_path = os.path.join(self.path, self.result['info_name']);
		if os.path.exists(self.target_path):
			print self.result['info_name'], "already exist";
			return None;
		else:
			os.makedirs(self.target_path);
			return True;

	def curl(self,url, type = None, proxy = None, data = None):
	    #print "download url:", 
	    headers = {'User-agent':self.default_agetnt};
	    request = urllib2.Request(url, data, headers=headers);

	    while self.num_retry > 0:

	        try:
	            html=  urllib2.urlopen(request).read();
	            host = urllib2.urlparse.urlparse(self.url).netloc.split('.');
	            break;
	        except urllib2.URLError as e:
	            print self.num_retry,'Download error:',e
	            if hasattr(e,'code') and  600 > e.code >= 320:
	                print("lalalal");
	            html = None;
	            self.num_retry = self.num_retry - 1;
	    return html;

	def download(self, url,dir,name=None):

	    if name == None:
	        defaultName = urllib2.urlparse.urlparse(url).path.split('/')[-1];
	    else:
	        defaultName = name;

	    if os.path.exists(dir):
	        pass
	    else:
	        os.mkdir(dir);
	    path = os.path.join(dir, defaultName); 

	    urllib.urlretrieve(url, path);


A = douban(1025194, "D:/python_save/douban/actor");	

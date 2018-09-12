# coding=utf-8
from selenium import webdriver
import time
import os
import requests;
import sys;

reload(sys) 
sys.setdefaultencoding('utf-8')

file = "./list.txt";
if os.path.exists(file):
	os.remove(file);

count = 0;

flag = 1;

path1 = "G:\\1_知乎\\知乎live";
path2 = "G:\\1_知乎\\知乎私家课";
path3 = "G:\\1_知乎\\视频live";


with open(file, "a") as f:
	for a in os.listdir(unicode(path1)):
		count += 1
		id   =  a.split('_')[-1].split('.')[0];
		name =  a.split('_')[-3].split('.')[0];
		user =  a.split('_')[-2].split('.')[0];
		f.write("%s - %8s  - %s\n" % (id, name, user))

print "total :%d" % count
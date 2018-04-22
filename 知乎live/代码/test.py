# coding=utf-8
import sys
import getliveinfo as glive;
import logging;

glive_config = {
	"username":"jushou2018@163.com",
	"password":"20140619fgt",
	"chromedirver":"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe",
	"savepath":"../download",
	"loginlevel":logging.INFO,
}





glive.setconfig(**glive_config);
glive.doit(927612860245364736,2);

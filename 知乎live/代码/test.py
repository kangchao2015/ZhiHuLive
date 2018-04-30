# coding=utf-8
import sys
import getliveinfo as glive;
import logging;

glive_config = {
	"username":"guansuo2018@163.com",
	"password":"kc80241546",
	"chromedirver":"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe",
	"savepath":"../download",
	"loginlevel":logging.INFO,
}





glive.setconfig(**glive_config);
glive.doit([924677414355890176],1);

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
#type 为1 的下载当前指定的live
#type 为2 的下载当前账号中的所有live
glive.doit(927610618117259264,1);

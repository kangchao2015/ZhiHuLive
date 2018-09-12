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

DEST_DIR = "D:\\ZhiHuLive\\知乎live\\zip";


a = [x for x in os.listdir(DEST_DIR)];

for z in a:
	print a;

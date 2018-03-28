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
import mysql.connector
from lxml import etree

reload(sys) 
sys.setdefaultencoding('utf-8')

aa = "本次 Live 中，我将在上一讲《线性代数入门：从方程到映射》的基础上，反其道而行之：从线性空间的结构与线性映射的直观本质入手，逐步引入「维数」、「直和分解」、「同构」等重要概念；并从线性映射的角度着重解释「矩阵的运算」是如何定义、以及方阵特征根与特征向量的本质含义，最终在「线性映射基本定理」处结束讲解，并从这个角度重新解 Cramer's Rule 的含义";
if isinstance(aa, str):
	print aa.replace("\'", "_");
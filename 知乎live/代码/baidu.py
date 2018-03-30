# encoding:utf-8
import base64
import urllib
import urllib2
import json;

'''
人脸探测
'''


token = "";
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GWAy6GnFrwljCDBTxQAoIZCQ&client_secret=iif31FfMrGZEFcihB4H40VHrg8B5w0ku'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    ret = json.loads(content);
    for a,b in ret.items():
        if a == "access_token":
            token = b;


print token;


request_url = "https://aip.baidubce.com/rest/2.0/face/v1/detect"

# 二进制方式打开图片文件
f = open('C:\\Users\\Think\\Desktop\\333.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"face_fields":"age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities","image":img,"max_face_num":12}
params = urllib.urlencode(params)

access_token = token;
request_url = request_url + "?access_token=" + access_token
request = urllib2.Request(url=request_url, data=params)
request.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urllib2.urlopen(request)
content = response.read()
if content:
    print content
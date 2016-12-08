#!coding=utf8

import json
import base64
import requests
import time
import re


user_pool = [	
		{"name":"18685873467","password":"pob1611"},
		{"name":"15685824264","password":"pob1611"},
		{"name":"17080651968","password":"abc123456"},
		{"name":"17032605804","password":"abc123456"},
		{"name":"17087005431","password":"abc123456"},
		{"name":"13263874144","password":"abc123456"},
		{"name":"17069162245","password":"abc123456"},
		{"name":"13263840132","password":"abc123456"},
		{"name":"17069160834","password":"abc123456"},
		{"name":"15577754637","password":"abc123456"},
		{"name":"17068965764","password":"abc123456"},
		{"name":"17077756236","password":"abc123456"},
		{"name":"17087001274","password":"abc123456"},
		{"name":"17077756175","password":"abc123456"}	
	]
	
user_info = "user_info"
with open('user.txt','rb') as f:
	user_info = f.read()

user_info = re.findall('.+',user_info)

for i in user_info:
	items = {}
	items["name"] = re.sub(":.+","",i)
	items["password"] = re.sub(".+:","",i)
	user_pool.append(items)

print "there are %d counts user_infos\n"%len(user_pool)

#用这个账号密码的作用就是获取一个有效的cookie，可以说是凭证

def getCookie(my_user_pool):
	cookies = []
	login_Url = r"https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)"
	log = open("./log.txt","a")
	for user in my_user_pool:
		name = user["name"]
		password = user["password"]
		username = base64.b64encode(name.encode('utf-8')).decode('utf-8')
		postData = {
				"entry": "sso",
				"gateway": "1",	
				"from": "null",
				"savestate": "30",
				"useticket": "0",
				"pagerefer": "",
				"vsnf": "1",
				"su": username,
				"sp": password,
				"service": "sso",
				"sr": "1440*900",
				"encoding": "UTF-8",
				"cdult": "3",
				"domain": "sina.com.cn",
				"prelt": "0",
				"returntype": "TEXT"
				}
	
		session = requests.Session()
		res = session.post(login_Url,data = postData)
		return_str = res.content.decode('gbk')
		info = json.loads(return_str)
		if info['retcode'] == "0":
			print "Get a Cookie Success!!!(By phoneNum = %s)" % name
			#print >> log,"At time %s , Get a Cookie Success!!!(By phoneNum = %s)" % (time.ctime,name)
			cookie = session.cookies.get_dict()
			cookies.append(json.dumps(cookie))
		else:
			print "ERROR , not get cookie , the Reason is %s" % info['reason']
			#print >> log,"At time %s , failed to get cookie , Reault = %s" % (time.ctime,info['reason'])
	return cookies




cookies = getCookie(user_pool)


for cookie in cookies:
		f = open("mycookies.json","a")
		f.write(cookie)
		f.close()

print "Get Cookies Finish! All count = %d" % len(cookies)
#print >> log,"Get Cookies Finish! All count = %d" % len(cookies)

		




	




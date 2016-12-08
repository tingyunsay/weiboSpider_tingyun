# -*- coding:utf-8 -*-

import requests
import re
import json
import random
from bs4 import BeautifulSoup
#import pickle
import time
from selenium import webdriver
import codecs
import lxml
import traceback

#temp=res.replace("\\n","").replace("\\t","").replace(" ","").replace("\\","").replace("\n","")
#res.replace("\\r","").replace("\\n","").replace("\\t","").replace("\\","").replace("\n","")

#url = "http://d.weibo.com/1087030002_2975_1003_0"
#url="http://weibo.com/yogalin?refer_flag=1087030701_2975_1003_0&is_hot=1"
#url="http://d.weibo.com/1087030002_2975_1003_0?page=2"
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"}

#req = requests.get(url,headers=headers)
cookies = [
]


#这里必须得使用json来读取，直接read文件会出错
def get_cookies(file_path):
	with open(file_path) as f:
		cookies_count = []
		data = f.read()
		res = re.findall('{.+?}',data)
		for i in res:
			cookies_count.append(json.loads(i))
		f.close()
	return cookies_count

def del_cookie(cookie):
	if cookie in cookies:
		cookies.remove(cookie)

def format_html(html_str):
	return html_str.replace("\\r","").replace("\\n","").replace("\\t","").replace("\\","").replace("\n","").replace(" ","")

def get_urls(url):
	urls = []
	for i in range(1,175):
			urls.append(url+"?page=%s"%i)
	return urls


def get_stars_index(all_page):
	myres = []
	tmp_cookie = random.choice(cookies)
	res = requests.get(all_page,cookies=tmp_cookie)
	#soup = BeautifulSoup(res.content,'lxml')
	#print target_script
	temp = format_html(res.content)
	result = re.findall('(?<=<dtclass="mod_pic"><ahref=\").+?\"',temp)
	for i in result:
			myres.append(re.sub("com","cn",i))
	return myres,tmp_cookie

#针对pc版
def get_detail(signal_page):
	res = requests.get(signal_page,cookies=random.choice(cookies))
	soup = BeautifulSoup(res.content,'lxml')
	target_name = re.search(".*?，",soup.select('meta[name=keywords]')[0].attrs['content'].encode('utf-8')).group()
	#第一项
	target_name = unicode(target_name,'utf-8')
	#print target_name
	stars_name = re.sub(u"\uff0c",u"",target_name)
	temp = res.content.replace("\\r","").replace("\\n","").replace("\\t","").replace("\\","").replace("\n","").replace(" ","")
	two_res = re.findall('(?<=<strongclass="W_f14">)\d+',temp)
	#第二第三项
	fans_nums = two_res[1]
	weibo_nums = two_res[2]
	#print two_res
	#print "usernam:%s , fans:%s , weibo:%s"%(stars_name,fans_nums,weibo_nums)
	items = {}
	items['stars_name'] = stars_name
	items['fans_num'] = fans_nums
	items['weibo_nums'] = weibo_nums
	return items


def url_pc2mobie(url_list):
	res = []
	for i in url_list:
			res.append(re.sub("com","cn",i))
	return res

#信息保存，以追加形式写入json
def storage_info(signal_star):
	f = codecs.open("./storage_info.json","a",encoding="utf-8")
	line = json.dumps(dict(signal_star),ensure_ascii=False)+"\n"
	f.write(line)
	



#针对移动端
def get_detail2(all_page):
	for signal_page in all_page:
		tmp_cookie = random.choice(cookies)
		res = requests.get(signal_page,cookies=tmp_cookie)
		soup = BeautifulSoup(res.content,'lxml')
		#昵称
		stars_name = ""
		try:
			stars_name = re.sub('\\xa0.+',"",soup.select('.ut > span:nth-of-type(1)')[0].text)
			#第二第三项
			weibo_nums = re.search('\d+',soup.select('.tip2 > .tc')[0].text).group()
			fans_nums = re.search('\d+',soup.select('.tip2 > a:nth-of-type(2)')[0].text).group()
		except:
			with open("log.txt",'a') as f:
				traceback.print_exc(file=f)
   				f.flush()
				f.write("Error page is %s"%signal_page)
   				f.close()
		#print "usernam:%s , fans:%s , weibo:%s"%(stars_name,fans_nums,weibo_nums)
		items = {}
		items['stars_name'] = stars_name
		items['fans_num'] = fans_nums
		items['weibo_nums'] = weibo_nums
		yield items
		


if __name__=="__main__":
	
	#all_urls = ["http://weibo.cn/ljljlj?refer_flag=1087030701_2975_1003_0",
	#			"http://weibo.cn/yogalin?refer_flag=1087030701_2975_1003_0",
	#			"http://weibo.cn/210926262?refer_flag=1087030701_2975_1003_0"
	#			]
	cookies = get_cookies("./mycookies.json")
	
	url = "http://d.weibo.com/1087030002_2975_1003_0"
	'''
	page_1 = get_stars_index(url)
	print len(page_1)
	for i in page_1:
			print i
	'''
	all_urls = get_urls(url)
	#get_stars_index(url)
	#url1 = "http://weibo.com/yogalin?refer_flag=1087030701_2975_1003_0&is_all=1"
	#url2 = "http://weibo.cn/yogalin?refer_flag=1087030701_2975_1003_0&is_all=1"
	print "All cookies numbers : %d"%len(cookies)

	page_numbers = 0
	for signal_url in all_urls:
			temp_html,tmp_cookie = get_stars_index(signal_url)
		
			#出现一个无效的cookies，设计一个借口，将这个cookeis从cookies池中del
			while len(temp_html) == 0:
				del_cookie(tmp_cookie)
				temp_html,tmp_cookie = get_stars_index(signal_url)

			print "正在爬取%d页~~~%d页的数据........"%(page_numbers,page_numbers+len(temp_html))
	
			page_numbers += len(temp_html)
			for items in get_detail2(temp_html):
				storage_info(items)
			print "现在还剩%d个有效cookies"%len(cookies)
	print "爬取完成。"


	
"""
前面的url依旧需要使用先抓取PC端，得出来一批新的detail urls，之后该换成移动端，爬取
"""

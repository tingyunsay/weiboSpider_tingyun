# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import requests
import re
import json
import random
from bs4 import BeautifulSoup
import threading
import logging
import twisted
import MySQLdb
#import pickle
import time
from selenium import webdriver
import codecs
import lxml
import traceback
from Queue import Queue 
from threading import Thread

#temp=res.replace("\\n","").replace("\\t","").replace(" ","").replace("\\","").replace("\n","")
#res.replace("\\r","").replace("\\n","").replace("\\t","").replace("\\","").replace("\n","")
headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36"}
cookies = []
star_names = set()
#conn = MySQLdb.connect('192.168.1.50','liaohong_w','liaohong_w','liaohong_test')
conn = MySQLdb.connect('127.0.0.1','root','liaohong','liaohong_test',charset='utf8')
cur = conn.cursor()
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
			#print "page i s:%s"%re.sub("com","cn",i)
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

def storage_info_mysql(signal_star):
	#conn = MySQLdb.connect('192.168.1.50','liaohong_w','liaohong_w','liaohong_test')
	#cur = conn.cursor()
	#cur.execute("create table if not exists weibo_stars(stars_name id PRIMARY ,)")
	cur.execute('insert INTO weibo_stars(stars_name,fans_nums,weibo_nums) VALUES ("%s","%s","%s")'%(signal_star['stars_name'],signal_star['fans_nums'],signal_star['weibo_nums']))

def handle_error(e):
	logging.err(e)


def before_storage(star_name):
	if star_name in star_names:
		f = open("log.txt","a")
		print >> f,"%s ,ERROR,The stars named %s is overread , Throw it!!!!"%(time.ctime(),star_name)
		return "ERROR"
	else:
		star_names.add(star_name)
		return "TRUE"
#针对移动端
def get_detail2(signal_page):
	#for signal_page in all_page:
	#print "crawl page is :%s"%signal_page
	#想明白了，原来是这边的cookies也有可能是失效的，我们也需要作一次判断，失败就删除此cookies，重新请求
	tmp_cookie = random.choice(cookies)
	res = requests.get(signal_page,cookies=tmp_cookie)
	while re.search(r'login.sina.com.cn',res.url):
			del_cookie(tmp_cookie)
			tmp_cookie = random.choice(cookies)
			res = requests.get(signal_page,cookies=tmp_cookie)
	soup = BeautifulSoup(res.content,'lxml')
	stars_name = ""
	weibo_nums = ""
	fans_nums = ""
	try:
		stars_name = re.sub('\\xa0.+',"",soup.select('.ut > span:nth-of-type(1)')[0].text)
		weibo_nums = re.search('\d+',soup.select('.tip2 > .tc')[0].text).group()
		fans_nums = re.search('\d+',soup.select('.tip2 > a:nth-of-type(2)')[0].text).group()
	except:
		with open("log.txt",'a') as f:
			traceback.print_exc(file=f)
			f.flush()
			f.write("\n%s ,Error page is %s"%(time.ctime(),signal_page))
			f.close()
	#print "usernam:%s , fans:%s , weibo:%s"%(stars_name,fans_nums,weibo_nums)
	items = {}
	items['stars_name'] = stars_name.encode('utf-8')
	#print stars_name
	items['fans_nums'] = fans_nums.encode('utf-8')
	items['weibo_nums'] = weibo_nums.encode('utf-8')
	#正确才处理
	#if "TRUE" == before_storage(items['stars_name']) and items['stars_name'] != "":
	storage_info(items)
		#storage_info_mysql(items)
	time.sleep(0.3)
	#yield items
	#return items

class ThreadWorker(Thread):
	def __init__(self,queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
				item = self.queue.get()
				if item is None:
						break
				get_detail2(item)
				self.queue.task_done()

if __name__=="__main__":
	cookies = get_cookies("./mycookies.json")
	url = "http://d.weibo.com/1087030002_2975_1003_0"
	all_urls = get_urls(url)
	print "All cookies numbers : %d"%len(cookies)
	page_numbers = 0
	threads = []

	queue = Queue()
	tasks = []
	for signal_url in all_urls:
			temp_html,tmp_cookie = get_stars_index(signal_url)
			#出现一个无效的cookies，设计一个借口，将这个cookeis从cookies池中del
			while len(temp_html) == 0:
				del_cookie(tmp_cookie)
				temp_html,tmp_cookie = get_stars_index(signal_url)
			for i in temp_html:
					tasks.append(i)
			#print "正在爬取%d页~~~%d页的数据........"%(page_numbers,page_numbers+len(temp_html))
			print "正在创建%d页~~~%d页的线程任务........"%(page_numbers,page_numbers+len(temp_html))
			page_numbers += len(temp_html)
			print "At time %s , 创建%d个任务完成，准备爬取......"%(time.ctime(),len(threads))
	
	for x in range(10):
			worker = ThreadWorker(queue)
			worker.daemon = True
			worker.start()
	for task in tasks:
			queue.put((task))
	queue.join()
	
	#for t in threads:
	#	t.setDaemon(True)
	#	t.start()
	#for t in threads:
	#	t.join()
	print "现在还剩%d个有效cookies"%len(cookies)
	print "爬取完成。"


	
"""
前面的url依旧需要使用先抓取PC端，得出来一批新的detail urls，之后该换成移动端，爬取
"""

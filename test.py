# -*- encoding: utf-8 -*-
import datetime
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
from datetime import datetime,timedelta
d1 = datetime.now()
d2 = d1+timedelta(seconds=10)
print d2.strftime("%Y-%m-%d %H:%M:%S")

# from lxml import etree
# from lxml import html
# import requests

# page = requests.get('https://baidu.com')
# # cc = (page.html)
# tree = etree.tostring(page.text.encode('utf-8'))
# root = tree.getroot()
# print root
# # tree = html.fromstring(page.text)
# print tree
# selector = etree.HTML(page.text)
# root = etree.Element("body")
# print list(root.getchildren())
# hrefs = page.xpath(u"//a")

# for href in hrefs:
#     print href.attrib
# from get_all_node_xpath import *
 
 
# def get_tree_max_deepth(all_xpath_list):
#     '''
#     得到一个HTML页面形成的xpath列表中最大长度，即DOM树的最大深度
#     '''
#     tree_deepth_list=[]
#     for one_xpath in all_xpath_list:
#         tree_deepth_list.append(len(one_xpath.split('/')[1:]))
#     return max(tree_deepth_list)
 
 
# if __name__ == '__main__':
# 	with open('../baidu.txt') as f:
# 		baidu=f.read()
# 	baidu_tree, baidu_xpath_list=get_clean_allnodes_xpath(baidu)
# 	max_tree_deepth=get_tree_max_deepth(baidu_xpath_list)
# 	for one_xpath in baidu_xpath_list:
# 		print one_xpath
    # print 'max_tree_deepth is:', max_tree_deepth

















# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
# sched = BackgroundScheduler()
# # 装饰器
# @sched.scheduled_job('interval', id='my_job_id', seconds=5)
# def job_function():
#     print("Hello World")

# @sched.scheduled_job('interval', id='my_job_id1', seconds=3)
# def job_function1():
#     time.sleep(10)
#     print("World Hello")

# # 开始
# sched.start()

# try:
#     # 模拟主进程持续运行
#     while True:
#         time.sleep(2)
#         print 'sleep'
# except(KeyboardInterrupt, SystemExit):
#     # Not strictly necessary if daemonic mode is enabled but should be done if possible
#     sched.shutdown()
#     print('Exit The Job!')

# import pickle
# # from powerline.segments.vim import tab
# table = {'a':[1,2,3],'b':[5,6,7],'c':['e','r','t']}
# # table =[1,2,3]
# print (type(table))
# mydb = open('ttt','rb')
# # pickle.dump(table,mydb)
# print pickle.load(mydb)
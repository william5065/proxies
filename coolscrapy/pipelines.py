# -*- coding: utf-8 -*-

# Define your item pipelines here
# centos安装MySQL-python，root用户下
# yum install mysql-devel
# pip install MySQL-python
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import time
# import redis
import json
import logging
from contextlib import contextmanager

from scrapy import signals, Request
from scrapy.exporters import JsonItemExporter
# from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from models import db_connect, create_news_table, PorxyAddress
from utils import check_proxy,check_proxy_update,check_proxy_amazon

from multiprocessing import freeze_support,Pool

from functools import partial
from sqlalchemy import desc,asc
# Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
_log = logging.getLogger(__name__)




@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ProxyDatabasePipeline(object):
    """Proxy Address记录保存到数据库"""

    def __init__(self):
        print("DDDDD")
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        print (self.Session)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        print("Proxy Address 记录保存到数据库 start")
        # pass

    def process_item(self, item, spider):
        # logging.info("Proxy Address 记录保存到数据库 start....")
        print("Proxy Address 记录保存到数据库 start....")
        url = item['protocol'] + "://"+item['ip'] +":"+item['port']
        proxy_address = PorxyAddress(proxy_address=url,
                          position=item['position'],
                          ptype=item['protocol'],
                          speed=item['speed'],
                          anonymity=item['anonymity'],
                          deleted=0
                          )
        with session_scope(self.Session) as session:
            if session.query(PorxyAddress).filter(PorxyAddress.proxy_address == url,PorxyAddress.deleted==0).all():
                logging.info("已经有重复数据,不再更新...")
                print("已经有重复数据,不再更新...")

            if session.query(PorxyAddress).filter(PorxyAddress.proxy_address == url,PorxyAddress.deleted==1).all():
                session.query(PorxyAddress).filter(PorxyAddress.proxy_address == url).update({'deleted' : 0})
                logging.info("已经有重复数据,代理又重新有效，...")
                print("再次更新...") 
                
            else:   
                session.add(proxy_address)
                logging.info("proxy_address.id=, {}".format(proxy_address.id))
        
                logging.info("将ProxyAddress记录保存到数据库 end....")
        
    
    def get_proxy_list(self):
        with session_scope(self.Session) as session:
            freeze_support()
            print("+++++++++++++")
            tmplist = session.query(PorxyAddress.proxy_address).all()           
            proxy_adds = [i[0] for i in tmplist]
            pass_urls =[]          
            ####
            PROCESSES = 10
            print ('Creating pool with %d processes\n' % PROCESSES)
            pool = Pool(PROCESSES)
            results = []         
            res = pool.map_async(check_proxy_update, proxy_adds)

            pool.close() 
            pool.join()
            if res.ready():
                if res.successful():
                    results = res.get()
                    print('------')
                    print (results)
                    pass_urls =results.remove('-1')
                    for i in proxy_adds:
                        print(i in pass_urls)
                        if i in pass_urls:
                            session.query(PorxyAddress).filter(PorxyAddress.proxy_address == i).update({'deleted' : 0})
                        else:
                            session.query(PorxyAddress).filter(PorxyAddress.proxy_address == i).update({'deleted' : 1})
            return "finish updted"
    
    def get_pass_urls(self,count):
        
        with session_scope(self.Session) as session:
            tmplist = session.query(PorxyAddress.proxy_address).filter(PorxyAddress.deleted == 0).order_by(asc(PorxyAddress.speed)).all()
            proxy_adds = [i[0] for i in tmplist]
            return proxy_adds[:(int(count))]
    
    # def get_proxys_by_special_url(self,special_url):
        
    #     with session_scope(self.Session) as session:
    #         freeze_support()
    #         tmplist = session.query(PorxyAddress.proxy_address).filter(PorxyAddress.deleted == 0).all()
    #         proxy_adds = [i[0] for i in tmplist]
            
    #         protocol = special_url.split(':')[0]
    #         print("ppppp")
    #         print(protocol)
    #         proxy_adds = [i for i in proxy_adds if protocol == i.split(':')[0]]
    #         print("___________")
    #         print(proxy_adds)

    #         pass_urls =[]          
    #         ####
    #         PROCESSES = 5
    #         print ('Creating pool with %d processes uu\n' % PROCESSES)
    #         pool = Pool(PROCESSES)
    #         results = []
            
    #         # length = len(proxy_adds)
    #         # special_url_list=[special_url]*length
    #         # print(special_url_list)
    #         # print("___________")
           
    #         # x_y = zip(special_url_list, proxy_adds)
    #         # print(x_y)  
    #         res = pool.map_async(check_proxy_amazon, proxy_adds)

    #         pool.close() 
    #         pool.join()
    #         if res.ready():
    #             if res.successful():
    #                 results = res.get()
    #                 if '-1' in results:
    #                     pass_urls =results.remove('-1')
    #         print("async finish")
    #         return pass_urls

    def close_spider(self, spider):
        print("*********")
        pass


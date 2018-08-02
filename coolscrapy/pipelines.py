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

from log_init import Log
logg = Log()


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
        logg.info("Init ProxyDatabasePipeline")
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        logg.info(self.Session)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        # print("Proxy Address 记录保存到数据库 start")
        logg.info("The spider is opened")
        # pass

    def process_item(self, item, spider):
        # logging.info("Proxy Address 记录保存到数据库 start....")
        logg.info("Proxy Address 记录保存到数据库 start....")
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
                logg.info("已经有重复数据,不再更新...")
                

            if session.query(PorxyAddress).filter(PorxyAddress.proxy_address == url,PorxyAddress.deleted==1).all():
                session.query(PorxyAddress).filter(PorxyAddress.proxy_address == url).update({'deleted' : 0})
                logg.info("Update the proxy_address :")
                logg.info(proxy_address)
                logg.info("已经有重复数据,代理又重新有效，...") 
                
            else:   
                session.add(proxy_address)
                logg.info("Add the proxy_address :")
                logg.info(proxy_address)
                logg.info("将ProxyAddress记录保存到数据库 end....")
        
    
    def get_proxy_list(self):
        with session_scope(self.Session) as session:
            freeze_support()
            logg.info("+++++++++++++")
            tmplist = session.query(PorxyAddress.proxy_address).all()           
            proxy_adds = [i[0] for i in tmplist]
            logg.info("proxy_adds")
            logg.info(proxy_adds)
            pass_urls =[]          
            ####
            PROCESSES = 10
            logg.info('Creating pool with %d processes\n' % PROCESSES)
            pool = Pool(PROCESSES)
            results = []         
            res = pool.map_async(check_proxy_update, proxy_adds)

            pool.close() 
            pool.join()
            if res.ready():
                if res.successful():
                    results = res.get()
                    
                    # pass_urls =results.remove('-1')
                    
                    pass_urls = [x for x in results if x!=None and x!='-1']
                    logg.info("Filte Pass Urls")
                    logg.info(pass_urls)
                    for i in proxy_adds:
                        if i in pass_urls:
                            session.query(PorxyAddress).filter(PorxyAddress.proxy_address == i).update({'deleted' : 0})
                        else:
                            session.query(PorxyAddress).filter(PorxyAddress.proxy_address == i).update({'deleted' : 1})
            return "finish updted"
    
    def get_pass_urls(self,count):
        
        with session_scope(self.Session) as session:
            tmplist = session.query(PorxyAddress.proxy_address).filter(PorxyAddress.deleted == 0).order_by(asc(PorxyAddress.speed)).all()
            proxy_adds = [i[0] for i in tmplist]
            logg.info("Get Pass URL:")
            logg.info(proxy_adds)
            return proxy_adds[:(int(count))]
    

    def close_spider(self, spider):
        print("*********")
        pass


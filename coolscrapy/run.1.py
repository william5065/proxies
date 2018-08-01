#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""

import logging
from twisted.internet import reactor
from twisted.web import server
from txrestapi.resource import APIResource
from txrestapi.methods import GET, POST, PUT, ALL
from twisted.internet.task import deferLater

from twisted.internet import task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from models import db_connect
from models import create_news_table
from models import ArticleRule
from sqlalchemy.orm import sessionmaker
from pipelines import ProxyDatabasePipeline
from spiders.kuaidaili_spider import KuaidailiSpider
from spiders.s31f_spider import S31fSpider
from spiders.xicidaili_spider import XicidailiSpider
from spiders.s89ip_spider import S89ipSpider
from spiders.yqie_spider import YqieSpider

from spiders.joke_spider import JokerSpider

# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
class ProxyAdressApi(APIResource):
    
    def _scan_proxy_job(self):
        pa = ProxyDatabasePipeline()
        str_back = pa.get_proxy_list()
        # pa.update_proxy_list(lists)
    
        return (str_back)

    def _scrapy_job(self):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        runner.crawl(KuaidailiSpider)
        runner.crawl(S31fSpider)
        runner.crawl(XicidailiSpider)
        runner.crawl(S89ipSpider)
        runner.crawl(YqieSpider)
        d = runner.join()
        

        # d.addBoth(lambda _:reactor.stop())
    def _scheduler_task(self):
        # # BlockingScheduler
        # scheduler = BlockingScheduler()
        scheduler = BackgroundScheduler()
        # scheduler.add_job(self.job, 'cron', day_of_week='1-5', hour=6, minute=30)
        scheduler.add_job(self._scrapy_job, 'interval', hours=6)
        scheduler.add_job(self._scan_proxy_job, 'interval', minutes=1)
        scheduler.start()
        # l = task.LoopingCall(self._scan_proxy_job)
        # l.start(180.0) # call every second



 
 
    

    @GET("/api/get/proxyadd")
    def get_proxyadd(self, request):
        self._scheduler_task()
        # d = deferLater(reactor, 5, lambda: request)
        # d.addCallback(self._scheduler_task)
        return 'NOT_DONE_YET'
   
 
    @POST("/path2")
    def path2(self, request):
        return "path2"
    
    
    @ALL("/api/getproxyaddress")
    def default(self, request):

        return '_scan_proxy'
 
 
if __name__ == "__main__":
    # os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"]='YES'
    site = server.Site(ProxyAdressApi())
    reactor.listenTCP(8080, site)
    reactor.run()






# if __name__ == '__main__':
#     settings = get_project_settings()

#     runner = CrawlerRunner(settings)
#     runner.crawl(KuaidailiSpider)
#     runner.crawl(S31fSpider)
#     runner.crawl(XicidailiSpider)
#     runner.crawl(S89ipSpider)
#     runner.crawl(YqieSpider)
    
#     d = runner.join()
#     d.addBoth(lambda _:reactor.stop())
    
#     reactor.run() # the scri

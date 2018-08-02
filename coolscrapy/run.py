#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""

# import tornado.ioloop
# import tornado.web


from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from pipelines import ProxyDatabasePipeline

from scrapy.utils.log import configure_logging
from pipelines import ProxyDatabasePipeline
from spiders.kuaidaili_spider import KuaidailiSpider
from spiders.s31f_spider import S31fSpider
from spiders.xicidaili_spider import XicidailiSpider
from spiders.s89ip_spider import S89ipSpider
from spiders.yqie_spider import YqieSpider
from twisted.internet import reactor

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from twisted.web.resource import Resource, NoResource

from twisted.web import server 
from txrestapi.resource import APIResource 

from txrestapi.methods import GET, POST, PUT, ALL, DELETE 

from utils import response_json

from log_init import Log
logg = Log()

class MainResource(APIResource):

    def _get_proxy_address(self):
        pa = ProxyDatabasePipeline()
        pa.get_proxy_list()
        str_back = pa.get_pass_urls(20)
        # pa.update_proxy_list(lists)
    
        return (str_back)
    
    def _scan_proxy_job(self):
        pa = ProxyDatabasePipeline()
        str_back = pa.get_proxy_list()
        # pa.update_proxy_list(lists)
    
        return (str_back)
    
    def _scrapy_job(self):
        
        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logg.info("Scrapy Start")

        configure_logging()
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
        scheduler = BackgroundScheduler()      
        # scheduler.add_job(self.job, 'cron', day_of_week='1-5', hour=6, minute=30)
        # scheduler.add_job(self._scrapy_job,'interval', minutes=40)
        
        # scheduler.add_job(self._scrapy_job, 'date', run_date='2018-08-02 10:36:01')
        logg.info("Scheduler Task Start")
        scheduler.add_job(self._scan_proxy_job,'interval', minutes=40)
        # scheduler.add_job(self._scan_proxy_job, 'date', run_date='2018-07-31 21:54:01')
     
        scheduler.start()


 
    @GET("/schedulertask")
    def path1(self, request):
        self._scheduler_task()
        return "path1"
 
    # @POST("/path2")
    # def path2(self, request):
    #     return "path2"
 
    @ALL("/geturls")
    def default(self, request):
        data = self._get_proxy_address()
        logg.info("Success to return urls")
        logg.info(data)
        return response_json(data,"OK","200")
 
 
if __name__ == "__main__":
    site = server.Site(MainResource())
    reactor.listenTCP(8080, site)
    reactor.run()


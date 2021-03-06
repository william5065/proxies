#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
# from scrapy.utils.log import configure_logging
from coolscrapy.spiders.kuaidaili_spider import KuaidailiSpider
from coolscrapy.spiders.s31f_spider import S31fSpider
from coolscrapy.spiders.xicidaili_spider import XicidailiSpider
from coolscrapy.spiders.s89ip_spider import S89ipSpider
from coolscrapy.spiders.yqie_spider import YqieSpider
from coolscrapy.pipelines import ProxyDatabasePipeline

from coolscrapy.utils import response_json

# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
import os,time
from twisted.internet import reactor,defer
import tornado.ioloop
import tornado.web
import datetime
from coolscrapy.log_init import Log
logg = Log()

class ProxyAdressHandler(tornado.web.RequestHandler):
    def _scan_database_address(self):
        stime = time.time()
        pa = ProxyDatabasePipeline()
        pa.get_proxy_list()
        etime = time.time()
        delta = etime - stime
    
        return datetime.timedelta(seconds=delta)

    def _scrapy_job(self):
        
        logg.info("Scrapy Start000")
        dfs = set()
        runner = CrawlerRunner(get_project_settings())

        for i in [KuaidailiSpider,S31fSpider,XicidailiSpider,S89ipSpider,YqieSpider]:
            dfs.add(runner.crawl(i))

        defer.DeferredList(dfs).addBoth(lambda _: reactor.crash())  

        reactor.run(installSignalHandlers=0)

    def _scheduler_task(self):    
        scheduler = TornadoScheduler(timezone="UTC") 
        # scheduler.add_job(self._scrapy_job,'interval', minutes=5)
        
        d1 = datetime.datetime.now()
        d2 = d1+datetime.timedelta(seconds=10)
        dates = d2.strftime("%Y-%m-%d %H:%M:%S")

        # scheduler.add_job(self._scrapy_job,'date', run_date=dates, args=[])

        scheduler.add_job(self._scrapy_job,'interval', minutes=50)

        # scheduler.add_job(self._scan_database_address,'date', run_date=dates, args=[])

        scheduler.add_job(self._scan_database_address,'interval', minutes=20)

        logg.info("Scheduler Task Start")
        scheduler.start()
        
    def get(self):
        self._scheduler_task()
        self.write("scheduler task start")

class ProxiesURLHandler(tornado.web.RequestHandler):
    
    def _get_proxy_urls(self):
        stime = time.time()
        pa = ProxyDatabasePipeline()
        data = pa.get_pass_urls(20)
        etime = time.time()
        delta = etime - stime
        logg.info("checked time:"+str(delta))
        return data
    
    def get(self):
        data = self._get_proxy_urls()
        self.write(response_json(data,"OK",200))

def make_app():
    return tornado.web.Application([
        (r"/scheduler", ProxyAdressHandler),
        (r"/getproxiesurls", ProxiesURLHandler),
    ])

if __name__ == "__main__":

    os.system('export SCRAPY_SETTINGS_MODULE=coolscrapy.settings')
    os.system('export PYTHONPATH=/var/data')
    os.system('source /etc/profile')

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

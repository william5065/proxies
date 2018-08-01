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

from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from pipelines import ProxyDatabasePipeline
from spiders.kuaidaili_spider import KuaidailiSpider
from spiders.s31f_spider import S31fSpider
from spiders.xicidaili_spider import XicidailiSpider
from spiders.s89ip_spider import S89ipSpider
from spiders.yqie_spider import YqieSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from tornado import gen
from tornado.concurrent import Future

from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource

from twisted.web import server 
from txrestapi.resource import APIResource 

from txrestapi.methods import GET, POST, PUT, ALL, DELETE 

from utils import response_json
import logging
logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
           datafmt='%a, %d %b %Y %H:%M:%S',
            filename='logs/spider.log',
            filemode='a')

class MainResource(APIResource):
    
    def _get_proxy_address(self):
        pa = ProxyDatabasePipeline()
        str_back = pa.get_pass_urls(20)
        # pa.update_proxy_list(lists)
    
        return (str_back)
    
    def _scan_proxy_job(self):
        pa = ProxyDatabasePipeline()
        str_back = pa.get_proxy_list()
        # pa.update_proxy_list(lists)
    
        return (str_back)
    
    def _scrapy_job(self):
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
        scheduler.add_job(self._scrapy_job,'interval', hours=3)
        # scheduler.add_job(self._scrapy_job, 'date', run_date='2018-07-31 21:23:01')
        scheduler.add_job(self._scan_proxy_job,'interval', minutes=20)
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
        
        return response_json(data,"OK","200")
 
 
if __name__ == "__main__":
    site = server.Site(MainResource())
    reactor.listenTCP(8080, site)
    reactor.run()






# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# Topic: sample
# Desc : 
# """

# import tornado.ioloop
# import tornado.web


# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from scrapy.utils.log import configure_logging
# from pipelines import ProxyDatabasePipeline
# from spiders.kuaidaili_spider import KuaidailiSpider
# from spiders.s31f_spider import S31fSpider
# from spiders.xicidaili_spider import XicidailiSpider
# from spiders.s89ip_spider import S89ipSpider
# from spiders.yqie_spider import YqieSpider
# from twisted.internet import reactor

# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
# from utils import response_json
# from tornado import gen
# from tornado.concurrent import Future

# class SchedulerTaskHandler(tornado.web.RequestHandler):
    
#     def _scan_proxy_job(self):
#         pa = ProxyDatabasePipeline()
#         str_back = pa.get_proxy_list()
#         # pa.update_proxy_list(lists)
    
#         return (str_back)

#     def _scrapy_job(self):
#         print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#         configure_logging()
#         settings = get_project_settings()
#         runner = CrawlerRunner(settings)
#         runner.crawl(KuaidailiSpider)
#         runner.crawl(S31fSpider)
#         runner.crawl(XicidailiSpider)
#         runner.crawl(S89ipSpider)
#         runner.crawl(YqieSpider)
#         d = runner.join()
#         d.addBoth(lambda _:reactor.stop())
#         reactor.run()

#     def _scheduler_task(self):

#         scheduler = BackgroundScheduler()
        
#         # scheduler.add_job(self.job, 'cron', day_of_week='1-5', hour=6, minute=30)
#         # scheduler.add_job(self._scrapy_job,'interval', hours=1)
#         # scheduler.add_job(self._scrapy_job, 'date', run_date='2018-07-25 21:06:01')
#         # scheduler.add_job(self._scan_proxy_job,'interval', minutes=20)
#         scheduler.add_job(self._scan_proxy_job, 'date', run_date='2018-07-29 08:54:01')
     
#         scheduler.start()




#     def get(self):
#         self._scheduler_task()
#         self.write('hellow')
 
#     def post(self):
#         return "path2"

# class ProxyListHandler(tornado.web.RequestHandler):
#     def get(self):
#         count = self.get_argument('count')
#         # url = self.get_argument('url')
#         # if url != None:
            
#         print count
#         pa = ProxyDatabasePipeline() 
#         data = pa.get_pass_urls(count)
#         response_json(data,"OK",200)
#         self.write(response_json(data,"OK",200))

# class ProxySpecialListHandler(tornado.web.RequestHandler):
#     @tornado.web.asynchronous
#     @tornado.gen.engine
#     def get(self):
#         future = Future()
        
#         url = self.get_argument('url')
#         print(url)

#         response =  yield tornado.gen.Task(self.res,url)
#         print  ("response:" ,response)
#         self.finish()
#         # future.add_done_callback(self.res,url)
#         # yield future
        
        
        
#     @tornado.gen.coroutine
#     def res(self,url):
#         pa = ProxyDatabasePipeline() 
#         data = pa.get_proxys_by_special_url(url)
#         print(data)
#         response_json(data,"OK",200)
#         return response_json(data,"OK",200)
        

# def make_app():
#     return tornado.web.Application([
#         (r"/api/get/proxy/list", ProxyListHandler),
#         (r"/api/get/scheduler/task", SchedulerTaskHandler),
#         (r"/api/get/special/proxy/list", ProxySpecialListHandler),    

#     ])

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8080)
#     tornado.ioloop.IOLoop.current().start()


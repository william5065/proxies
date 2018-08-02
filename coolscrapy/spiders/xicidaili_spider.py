# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# """
# Topic: 网络爬虫
# Desc :
# """
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 爬取虎嗅网首页
Desc : 
"""
from log_init import Log

import scrapy
from items import ProxyItem
from utils import check_proxy
from bs4 import BeautifulSoup
import re
import requests
logg = Log()
class XicidailiSpider(scrapy.Spider):
    name = "xicidaili"
    allowed_domains = ["xicidaili.com"]
    start_urls = ["http://www.xicidaili.com/nn/"+str(i)+"/" for i in range (1,5)]
    start_urls.extend(["http://www.xicidaili.com/nt/"+str(i)+"/" for i in range (1,5)])
    start_urls.extend(["http://www.xicidaili.com/wn/"+str(i)+"/" for i in range (1,5)])
    start_urls.extend(["http://www.xicidaili.com/wt/"+str(i)+"/" for i in range (1,5)])
    

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        sites =soup.findAll('tr')

        logg.info (response.url)
        for sel in sites:
            if sel.find(text =re.compile(r'\d+\.\d+\.\d+\.\d+')):
                logg.info(sel)
                item = ProxyItem()
                item['ip'] = sel.findAll('td')[1].text.strip()
                logg.info (item['ip'] )
                item['port'] = sel.findAll('td')[2].text.strip()
                logg.info (item['port'])
                # url = response.urljoin(item['link'])
                if 'http-proxy' in response.url:
                    item['protocol'] = "http"
                    logg.info (item['protocol'])
                else:
                    item['protocol'] = sel.findAll('td')[5].text
                    logg.info (item['protocol'])
                item['position'] = sel.findAll('td')[3].text.strip()
                logg.info (item['position'])
                proxies ={}
                item['anonymity'] = sel.findAll('td')[4].text
               
                url = item['protocol'] + "//:"+item['ip'] +":"+item['port']
                proxies[item['protocol']]=url
                item['protocol'] = item['protocol'].strip().lower()
                item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                logg.info("item['speed']:"+ item['speed'])
                if item['speed']!='-1' and item['speed']!= None:
                    yield item
                
                
                


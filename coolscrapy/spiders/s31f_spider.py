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

import scrapy
from coolscrapy.items import ProxyItem
from coolscrapy.utils import check_proxy
from bs4 import BeautifulSoup
import re
import requests
from coolscrapy.log_init import Log
logg = Log()
class S31fSpider(scrapy.Spider):
    name = "31f"
    allowed_domains = ["31f.cn"]
    start_urls = ["http://31f.cn/http-proxy/",
                  "http://31f.cn/https-proxy/",
                  "http://31f.cn/socks-proxy/"
                  ]

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        sites =soup.findAll('tr')

        # print (response.url)
        for sel in sites:
            if sel.find(text =re.compile(r'\d+\.\d+\.\d+\.\d+')):
                logg.info(sel)
                item = ProxyItem()
                item['ip'] = sel.findAll('td')[1].text
                logg.info (item['ip'] )
                item['port'] = sel.findAll('td')[2].text
                logg.info (item['port'])
                # url = response.urljoin(item['link'])
                if 'http-proxy' in response.url:
                    item['protocol'] = "http"
                    logg.info (item['protocol'])
                else:
                    item['protocol'] = sel.findAll('td')[6].text
                    logg.info (item['protocol'])
                item['position'] = sel.findAll('td')[3].text
                logg.info (item['position'])
                proxies ={}
                item['anonymity'] = 'DDD'
               
                url = item['protocol'] + "//:"+item['ip'] +":"+item['port']
                proxies[item['protocol']]=url
                item['protocol'] = item['protocol'].strip().lower()
                item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                logg.info("item['speed']:")
                logg.info(item['speed'])
                if item['speed']!='-1' and item['speed']!= None:
    
                    yield item
                
                
                


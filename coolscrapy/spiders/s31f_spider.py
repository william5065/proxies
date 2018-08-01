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
import logging
import scrapy
from items import ProxyItem
from utils import check_proxy
from bs4 import BeautifulSoup
import re
import requests

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

        print (response.url)
        for sel in sites:
            if sel.find(text =re.compile(r'\d+\.\d+\.\d+\.\d+')):
                # print(sel)
                item = ProxyItem()
                item['ip'] = sel.findAll('td')[1].text
                print (item['ip'] )
                item['port'] = sel.findAll('td')[2].text
                print (item['port'])
                # url = response.urljoin(item['link'])
                if 'http-proxy' in response.url:
                    item['protocol'] = "http"
                    print (item['protocol'])
                else:
                    item['protocol'] = sel.findAll('td')[6].text
                    print (item['protocol'])
                item['position'] = sel.findAll('td')[3].text
                print (item['position'])
                proxies ={}
                item['anonymity'] = 'DDD'
               
                url = item['protocol'] + "//:"+item['ip'] +":"+item['port']
                proxies[item['protocol']]=url
                item['protocol'] = item['protocol'].strip().lower()
                item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                if item['speed']!='-1' and item['speed']!= None:
                    yield item
                
                
                


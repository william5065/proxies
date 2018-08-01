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

class YqieSpider(scrapy.Spider):
    name = "yqie"
    allowed_domains = ["89ip.cn"]
    start_urls = ["http://ip.yqie.com/ipproxy.htm"]

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        sites =soup.findAll('tr')

        print (response.url)
        for sel in sites:
            if sel.find(text =re.compile(r'\d+\.\d+\.\d+\.\d+')):
                # print(sel)
                item = ProxyItem()
                item['ip'] = sel.findAll('td')[0].text.strip()
                print (item['ip'] )
                item['port'] = sel.findAll('td')[1].text.strip()
                print (item['port'])
                item['position'] = sel.findAll('td')[2].text.strip()
                print (item['position'])
                proxies ={}
                item['anonymity'] = sel.findAll('td')[3].text.strip()
                item['protocol'] =sel.findAll('td')[4].text.strip().lower()
                url = item['protocol'] + "//:"+item['ip'] +":"+item['port']
                proxies[item['protocol']]=url
                item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                if item['speed']!='-1' and item['speed']!= None:
                    yield item


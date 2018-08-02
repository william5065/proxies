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
from items import ProxyItem
from utils import check_proxy
from bs4 import BeautifulSoup
import re
import requests
from log_init import Log
logg = Log()

class YqieSpider(scrapy.Spider):
    name = "yqie"
    allowed_domains = ["89ip.cn"]
    start_urls = ["http://ip.yqie.com/ipproxy.htm"]

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        sites =soup.findAll('tr')

        logg.info (response.url)
        for sel in sites:
            if sel.find(text =re.compile(r'\d+\.\d+\.\d+\.\d+')):
                logg.info (sel)
                item = ProxyItem()
                item['ip'] = sel.findAll('td')[0].text.strip()
                logg.info  (item['ip'] )
                item['port'] = sel.findAll('td')[1].text.strip()
                logg.info  (item['port'])
                item['position'] = sel.findAll('td')[2].text.strip()
                logg.info  (item['position'])
                proxies ={}
                item['anonymity'] = sel.findAll('td')[3].text.strip()
                item['protocol'] = sel.findAll('td')[4].text.strip().lower()
                url = item['protocol'] + "//:"+item['ip'] +":"+item['port']
                proxies[item['protocol']] = url
                item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                logg.info("item['speed']:"+ item['speed'])
                if item['speed']!='-1' and item['speed']!= None:
                    yield item


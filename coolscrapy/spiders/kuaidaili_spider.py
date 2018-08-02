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

class KuaidailiSpider(scrapy.Spider):
    name = "kuaidaili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = ["https://www.kuaidaili.com/free/inha/"+str(i)+"/" for i in range (1,8)]

    def parse(self, response):
        data = response.body
        # print data
        soup = BeautifulSoup(data, "html5lib")
        # sites = soup.findAll('tr', text=re.compile("HTTP"))
        sites =soup.findAll('tr')
        # print sites
        for sel in sites:           
            if sel.find(text =re.compile(r'\d+\.\d+\.\d+\.\d+')):
                
                logg.info(sel)
                item = ProxyItem()
                # print (sel.xpath('h2/a/text()'))
                item['ip'] = sel.findAll('td')[0].text
                logg.info(item['ip'])
                item['port'] = sel.findAll('td')[1].text
                logg.info (item['port'])
                # url = response.urljoin(item['link'])
                item['protocol'] = sel.findAll('td')[3].text
                logg.info (item['protocol'])
                item['position'] = sel.findAll('td')[5].text
                logg.info (item['position'])
                proxies ={}
                item['anonymity'] = 'DDD'
                tmp = item['protocol']
                tmp = tmp.split(',')
                if len(tmp) ==2:
                    for i in tmp: 
                        url = i + "//:"+item['ip'] +":"+item['port']
                        proxies[i]=url
                        item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                        logg.info("item['speed']:"+ item['speed'])
                        if item['speed']!='-1'and item['speed']!=None:
                            item['protocol'] = i.strip().lower()
                            logg.info (item['protocol'])
                            yield item
                else:
                    url = item['protocol'] + "//:"+item['ip'] +":"+item['port']
                    proxies[item['protocol']]=url
                    item['protocol'] = tmp[0].strip().lower()
                    item['speed'] = check_proxy('https://www.amazon.com/',proxies)
                    if item['speed']!='-1' and item['speed']!= None:
                        yield item
                
                
                



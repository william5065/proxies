# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
    """Proxy Item"""
    ip = scrapy.Field()             # ip
    port = scrapy.Field()          # port
    protocol = scrapy.Field()     # protocol
    anonymity = scrapy.Field()     # anonymity
    speed = scrapy.Field()  # speed
    position = scrapy.Field()     # position
    
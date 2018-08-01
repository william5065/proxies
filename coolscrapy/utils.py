#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 一些工具类
Desc : 
"""
import re
import sys
import smtplib
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os.path
from settings import IMAGES_STORE
from models import db_connect, create_news_table
from sqlalchemy.orm import sessionmaker
import requests
import json
from multiprocessing import Process, Queue ,freeze_support,Pool

def check_proxy(check_url,proxies):     
    try:
        r = requests.get(check_url, proxies=proxies, timeout=3)
        if r.status_code == 200:
            r_time = str(r.elapsed.total_seconds())
            print('success'+str(r_time))
            return r_time
                 
    except:
        print('connect failed:-1')
        return str(-1)


def check_proxy_update(check_url):
    proxies = {}

    proxies[check_url.split(':')[0]] = check_url
    print(check_url)
    print(proxies)   
    try:
        # r = requests.get('https://www.ipip.net/', proxies=proxies, timeout=3)
        r = requests.get('https://www.amazon.com/', proxies=proxies, timeout=3)
        if r.status_code == 200:
            # r_time = str(r.elapsed.total_seconds())
            print('success'+str(check_url))
            return check_url
                 
    except:
        print('connect update failed:-1')
        return str(-1)

def check_proxy_amazon(check_url):
    proxies = {}

    proxies[check_url.split(':')[0]] = check_url
    print(check_url)
    print(proxies)   
    try:
        r = requests.get('https://www.amazon.com/', proxies=proxies, timeout=8)
        if r.status_code == 200:
            # r_time = str(r.elapsed.total_seconds())
            print('success'+str(check_url))
            return check_url
                 
    except:
        print('connect update failed:-1')
        return str(-1)

def check_special_proxy(special_url,proxy_url):
    proxies = {}
    proxies[proxy_url.split(':')[0]] = proxy_url
    print("+++++++++++++++++")
    print(special_url)
    print(proxy_url)
    print(proxies)   
    try:
        r = requests.get(special_url, proxies=proxies, timeout=3)
        if r.status_code == 200:
            # r_time = str(r.elapsed.total_seconds())
            print('success:::'+proxy_url)
            return proxy_url
                 
    except:
        print('connect update failed::::-1')
        return str(-1)

def response_json(data,msg,code):
    encode_json = json.dumps({'data':data,'msg':msg,'code':code})
    return encode_json

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc : 
"""
import datetime

# from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float,String, Text, DateTime
from coolscrapy.log_init import Log
logg = Log()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    logg.info("d0000")
    # DB_CONNECT_STRING = 'mysql+mysqldb://root:12345a@47.98.48.17:3306/tester?charset=utf8'
    DB_CONNECT_STRING = "mysql+pymysql://root:12345a@47.98.48.17:3306/tester"
    
    engine = create_engine(DB_CONNECT_STRING, max_overflow=5)
    # DB_CONNECT_STRING = 'mysql://root:12345a@47.98.48.17/tester?charset=utf8'
    logg.info(DB_CONNECT_STRING)
    # return create_engine(URL(**DATABASE))
    return engine


def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)


def _get_date():
    return datetime.datetime.now()

Base = declarative_base()




class PorxyAddress(Base):
    
    __tablename__ = 't_proxyaddress'

    id = Column(Integer, primary_key=True)
    proxy_address = Column(String(200))
    position = Column(String(32))
    ptype = Column(String(32))
    anonymity = Column(String(32))
    speed = Column(String(8))
    deleted = Column(Integer)
    created_time = Column(DateTime, default=_get_date)
    updated_time = Column(DateTime, default=_get_date,onupdate=_get_date)

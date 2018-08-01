#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc : 
"""
import datetime

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Float,String, Text, DateTime
from settings import DATABASE


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    print ("d0000")
    DB_CONNECT_STRING = 'mysql://root:12345a@47.98.48.17/tester?charset=utf8'
    # return create_engine(URL(**DATABASE))
    return create_engine(DB_CONNECT_STRING,echo=True)


def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)


def _get_date():
    return datetime.datetime.now()

Base = declarative_base()




class PorxyAddress(Base):
    """代理地址"""
    __tablename__ = 't_proxyaddress'

    id = Column(Integer, primary_key=True)
    proxy_address = Column(String(32))
    position = Column(String(32))
    ptype = Column(String(32))
    anonymity = Column(String(32))
    speed = Column(String(8))
    deleted = Column(Integer)
    created_time = Column(DateTime, default=_get_date)
    updated_time = Column(DateTime, default=_get_date,onupdate=_get_date)

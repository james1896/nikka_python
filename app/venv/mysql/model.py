# -*- coding: utf-8 -*-

import random

from app.config import Base
from sqlalchemy import DateTime
from sqlalchemy import Float, ForeignKey
from sqlalchemy import Column, Integer, String


#########################   User表结构    #####################################################


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    pwd = Column(String(120), unique=False)
    user_id = Column(String(40), unique=True)
    email = Column(String(120), unique=False)
    points = Column(Float, unique=False)
    first_time = Column(DateTime,unique=False)

    status = Column(Integer, unique=False)
    uuid = Column(String(120), unique=False)
    device = Column(String(50), unique=False)


    def __init__(self, name=None,pwd=None,user_id=None):
        self.name       = name
        self.pwd        = pwd
        self.user_id    = user_id
        self.email      = None
        self.points     = 0.0
        self.first_time  = None

        self.status     = 0
        self.uuid       ='uuid'
        self.device     ='device'



    # def __init__(self, name=None,pwd=None,email=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.email = email
    #
    # def __init__(self, name=None,pwd=None,points=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.points = points

    def __repr__(self):
        return '%s (%r, %r)' % (self.__class__.__name__, self.name, self.email)

#########################   Order 表结构    #####################################################

class Order(Base):
    __tablename__ = 'orders'

    id          = Column(Integer, primary_key=True)
    order_id    = Column(Integer, unique=True)
    deal_time   = Column(DateTime, unique=True)
    deal_Prce   = Column(Float,unique=False)
    goods_name  = Column(String(30),unique=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, user_id=None,deal_time=None,deal_Prce=None,goods_name=None):
        self.user_id = user_id
        self.deal_time = deal_time
        self.deal_Prce = deal_Prce
        self.goods_name = goods_name

        self.order_id = 10000+int(random.uniform(0, 1000000))

    # def __init__(self, name=None,pwd=None,email=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.email = email
    #
    # def __init__(self, name=None,pwd=None,points=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.points = points

    def __repr__(self):
        return '%s (%r, %r)' % (self.__class__.__name__, self.user_id, self.goods_name)

#########################   用户设备管理 表结构    #####################################################
class Userbehaviour(Base):
    __tablename__ = 'user_behaviour'

    id          = Column(Integer, primary_key=True)
    username    = Column(String(20), unique=False)
    last_time   = Column(DateTime, unique=False)
    uuid        = Column(String(120), unique=False)
    device      = Column(String(50), unique=False)
    ip          = Column(String(20), unique=False)

    # user_id     = Column(Integer, ForeignKey('users.id'))

    def __init__(self, last_time=None, username=None,uuid=None,device=None):

        self.username    = username
        self.last_time  = last_time
        self.uuid       = uuid
        self.device     = device


#########################   用户反馈 表结构    #####################################################
class FeedBack(Base):
    __tablename__ = 'feedback'
    id      = Column(Integer, primary_key=True)
    time    = Column(DateTime, unique=False)
    content = Column(String(500), unique=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self,time = None,content = None,user_id = None):
        self.time       = time
        self.content    = content
        self.user_id    = user_id

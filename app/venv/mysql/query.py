# -*- coding: utf-8 -*-
from .model import UserBehaviourStatistics
from app.config import  db_session

import datetime

def test():
    behaviour = UserBehaviourStatistics(login_time=datetime.datetime.now(),user_id=1)
    try:
        db_session.add(behaviour)
        db_session.commit()
    except Exception, e:
        print 'wrong'

def loginTime(user_id):
    behaviour = UserBehaviourStatistics(login_time=datetime.datetime.now(), user_id=user_id)
    try:
        db_session.add(behaviour)
        db_session.commit()
    except Exception, e:
        print ''


    # for i in range(0,1000000):
    #     addOrder(deal_Prce, goods_name):
    #     user_id = 1
    #     order = Order(user_id=user_id, deal_time=datetime.datetime.now(), deal_Prce=deal_Prce, goods_name=goods_name)
    #     try:
    #         db_session.add(order)
    #         db_session.commit()
    #     except Exception, e:
    #         return 0
    #     return 1
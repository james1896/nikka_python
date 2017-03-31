# -*- coding: utf-8 -*-
from .model import User,Order
from .model import UserBehaviourStatistics
from app.config import  db_session

import datetime
from sqlalchemy import func, extract

###########################################   master    ####################################################
###########################################   master    ####################################################
###########################################   master    ####################################################
###########################################   master    ####################################################

#查询某一天 某个月 某年 的数据

#该字段类型必需为  datetime
# 之后只需要这么写，就可以获取某月份的所有数据了
#
# 获取12月份的所有数据
# historys = History.query.filter(extract('month', History.date) == 12).all()


#month day year
def historyForLoginTime():
    historys = User.query.filter(extract('month', User.last_time) == 3).all()
    return historys


#查询order表 积分总数
def allPoints():
    #当前时间
    # print db_session.query(func.now()).scalar()
    #msyql sum方法
    return db_session.query(func.sum(Order.deal_Prce)).scalar()

#查询user表中有多少用户
def userCounts():
    try:
        count = db_session.query(User).filter_by().count()
    except Exception,e:
        count = -1
    return count


###########################################   master    ####################################################
###########################################   master    ####################################################
###########################################   master    ####################################################
###########################################   master    ####################################################

####################    积分转赠    ##############################################
#积分转赠

def pointGift(sponsor,received,point):
    spo = User.query.filter(User.user_id == sponsor).first()
    if spo:
        rec = User.query.filter(User.name == received).first()
        print 'received',rec.points
        if rec and spo.points > float(point):
            spo.points = spo.points-float(point)
            rec.points = rec.points+float(point)
            try:
                db_session.add(spo)
                db_session.add(rec)
                db_session.commit()
                return 1
            except Exception,e:
                print 0
        else:
            return
    return -1

##################################################################

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
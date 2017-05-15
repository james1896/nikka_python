# -*- coding: utf-8 -*-
import random

from app.venv.statuscode import status_code
from .model import User, Order, FeedBack
from .model import UserBehaviourStatistics
from app.config import  db_session

import datetime,time
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


# time.strftime('%Y-%m-%d',time.localtime(time.time()))
def historyForCurrentMonth():
    month = time.strftime('%m', time.localtime(time.time()))

    return histroyLoginInfo('month',month);

def historyForCurrentDay():
    day = time.strftime('%d', time.localtime(time.time()))
    return histroyLoginInfo('day',day);

#period   mounth,day,year
#number    12   31  2017
def histroyLoginInfo(period,number):
    historys = User.query.filter(extract(period, User.last_time) == number).all()
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


################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

def feedback(user_id,content):
    today = datetime.datetime.now()
    feed = FeedBack(today,content,user_id)
    try:
        db_session.add(feed)
        db_session.commit()
        return status_code.trueCode
    except Exception, e:
        print "feedback", e
        return status_code.query_feedback_failure

#注册接口
#
def register(name,pwd,uuid = None,device = None):
    # user_id = ticks%10000*100000*1000+1*1000
    today = datetime.datetime.now()
# 00000 000 000

    first = int(time.time())/100000
    second = int(random.uniform(0, 99))
    third = int(time.time())%100000%1000

    times = first*1000000 + second*1000 + third

    print times,'first:',first,'second',second,'third',third
    u = User(name = name, pwd= pwd,user_id=str(times))
    u.uuid = uuid
    u.device = device

    # print 'uuid',uuid
    u.last_time = today
    try:
        db_session.add(u)
        db_session.commit()
        return u
    except Exception,e:
        print "用户名 重复" , e
        return None

#登录接口
#
def login(name,pwd,uuid=None,device=None):
    try:
        u = User.query.filter(User.name==name).first()
    except Exception, e:
        return 'there isnot %s' % name

    if  u:
        if u.pwd == pwd:
            # points = User.query.filter(User.i==name).first()
            u.last_time = datetime.datetime.now()
            u.uuid = uuid
            u.device = device
            db_session.add(u)
            db_session.commit()
            return u
    else:
        return False
    
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

##################################################################################

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
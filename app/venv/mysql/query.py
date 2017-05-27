# -*- coding: utf-8 -*-
import random

from app.venv.statuscode import status_code
from .model import User, Order, FeedBack
from .model import Userbehaviour
from app.config import db_session

import datetime, time
from sqlalchemy import func, extract


###########################################   master    ####################################################
###########################################   master    ####################################################
###########################################   master    ####################################################
###########################################   master    ####################################################

# 查询某一天 某个月 某年 的数据

# 该字段类型必需为  datetime
# 之后只需要这么写，就可以获取某月份的所有数据了
#
# 获取12月份的所有数据
# historys = History.query.filter(extract('month', History.date) == 12).all()



# month day year
def historyForLoginTime():
    historys = User.query.filter(extract('month', User.last_time) == 3).all()
    return historys


# time.strftime('%Y-%m-%d',time.localtime(time.time()))
def historyForCurrentMonth():
    month = time.strftime('%m', time.localtime(time.time()))

    return histroyLoginInfo('month', month);


def historyForCurrentDay():
    day = time.strftime('%d', time.localtime(time.time()))
    return histroyLoginInfo('day', day);


# period   month,day,year
# number    12   31  2017
def histroyLoginInfo(period, number):
    historys = Userbehaviour.query.filter(extract(period, Userbehaviour.last_time) == number).all()
    return historys


# 查询order表 积分总数
def allPoints():
    # 当前时间
    # print db_session.query(func.now()).scalar()
    # msyql sum方法
    return db_session.query(func.sum(User.points)).scalar()


# 查询user表中有多少用户
def userCounts():
    try:
        count = db_session.query(User).filter_by().count()
    except Exception, e:
        count = -1
    return count

def getloginsAtOneDay():
    i = datetime.datetime.now()
    # interval = 1 day
    # interval = 2 month
    paras1 = "day"
    paras2 = "%s" % (i.day-2)

    return histroyLoginInfo("day",paras2)
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

def getid(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    return user.id


def findOrder(user_id):
    try:
        # order = Order.query.filter(Order.user_id == user_id).all()
        order = Order.query.filter(Order.user_id == user_id).limit(20)
        return order
    except Exception, e:
        print "findOrder", e
        return status_code.query_findorder_failure


# 用户信息收集
def userinfo(name, uuid, device):
    today = datetime.datetime.now()
    info = Userbehaviour(today, name, uuid, device)
    try:
        db_session.add(info)
        db_session.commit()
        return status_code.trueCode
    except Exception, e:
        print "userinfo", e
    return status_code.query_userinfo_failure


# 意见反馈
def feedback(user_id, content):
    today = datetime.datetime.now()
    feed = FeedBack(today, content, user_id)
    try:
        db_session.add(feed)
        db_session.commit()
        return status_code.trueCode
    except Exception, e:
        print "feedback", e
        return status_code.query_feedback_failure


# 注册接口
#
def register(name, pwd, uuid=None, device=None):
    # user_id = ticks%10000*100000*1000+1*1000
    today = datetime.datetime.now()
    # 00000 000 000


    first = int(time.time()) / 1000000 % 1000

    second = int(time.time()) / 1000 % 1000

    third = int(time.time()) % 1000

    times = first * 10000000 + second * 10000 + third * 10 - 3950000000 + int(random.uniform(0, 9))

    print "second", time.time(), id, times, 'first:', first, 'second', second, 'third', third

    # user_id为十位
    u = User(name=name, pwd=pwd, user_id=str(times))
    u.uuid = uuid
    u.device = device

    # print 'uuid',uuid
    u.last_time = today
    try:
        db_session.add(u)
        db_session.commit()
        return u
    except Exception, e:
        print "用户名 重复", e
        return None


# 登录接口
#
def login(name, pwd, uuid=None, device=None):
    try:
        u = User.query.filter(User.name == name).first()
    except Exception, e:
        return 'there isnot %s' % name

    if u:
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

    ###########################    更新积分接口    #############################################
    #

    # 如果paras ＝ 0 表示查询当前积分
    # 如果paras != 0 表示更改当前积分
def update_points(userid, positive_points, negative_points):
    if int(positive_points) == 0 and int(negative_points) == 0:
        try:
            u = User.query.filter(User.user_id == userid).first()
            print 'userName:', u.name, '积分', u.points
            return u
        except Exception, e:
            return status_code.query_points_select_failure

    elif positive_points > 0 and negative_points == 0:
        try:
            u = User.query.filter(User.user_id == userid).first()
            point = u.points + positive_points
            print "number:", positive_points
            u.points = point
            db_session.add(u)
            db_session.commit()
            return u
        except Exception, e:
            print e
            return status_code.query_points_update_failure
    elif positive_points == 0 and negative_points > 0:
        try:
            u = User.query.filter(User.user_id == userid).first()
            point = u.points - negative_points
            print "number:", negative_points
            if (point >= 0):
                u.points = point
                db_session.add(u)
                db_session.commit()
                return u
        except Exception, e:
            print e
            return status_code.query_points_update_failure
    else:
        return status_code.query_update_points_parameter_error


##################################################################

####################    积分转赠    ##############################################
# 积分转赠

def transformpoint(sponsor, received, point):
    spo = User.query.filter(User.user_id == sponsor).first()
    if spo:
        rec = User.query.filter(User.name == received).first()

        if rec and spo.points > float(point):
            spo.points = spo.points - float(point)
            rec.points = rec.points + float(point)
            try:
                db_session.add(spo)
                db_session.add(rec)
                db_session.commit()
                return status_code.trueCode
            except Exception, e:
                print status_code.query_points_transform_failuret
        else:
            return status_code.query_points_transform_received_failuret
    else:
        return status_code.query_points_transform_sponsor_failuret


        ##################################################################################
        #
        # def test():
        #     behaviour = UserBehaviourStatistics(login_time=datetime.datetime.now(),user_id=1)
        #     try:
        #         db_session.add(behaviour)
        #         db_session.commit()
        #     except Exception, e:
        #         print 'wrong'
        #
        # def loginTime(user_id):
        #     behaviour = UserBehaviourStatistics(login_time=datetime.datetime.now(), user_id=user_id)
        #     try:
        #         db_session.add(behaviour)
        #         db_session.commit()
        #     except Exception, e:
        #         print ''


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
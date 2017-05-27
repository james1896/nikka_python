# -*- coding: utf-8 -*-

import random

import datetime

from app.client.views import decryption
from app.venv.statuscode import status_code
from . import admin
from flask import jsonify, request, json
from app.config import init_db
from ..templates import sqlmodel
from app.config import db_session

from app.venv.rsa import rsaCipher

from ..venv.mysql import query



#这里要注意是admin.route (即对应蓝图的名称)
@admin.route('/')
def index():
    from ..venv.timer import scheduler
    return "hello admin"



# 得到当前顾客的登录情况
# interval = 1 day  当天登录用户数量
# interval = 2 mounth 当月登录用户数量
#
# interval = 0  返回 当天和当月
# {
#   "day": 2,
#   "month": 4
# }
@admin.route('/curusers',methods=['POST'])
def usersAt():
    # day = int(request.form['day'])
    interval = request.form['date']
    print 'interval:',isinstance(interval,str)

    i = datetime.datetime.now()
    print ("当前的年份是 %s" % i.year)

    # interval = 1 day
    # interval = 2 month
    paras1 = "day"
    paras2 = "%s" %i.day
    if interval == '2':
        paras1 = "month"
        paras2 = "%s" % i.month
        print ("当前的月份是 %s" % i.month)

    elif interval == '0':
        day = query.histroyLoginInfo('day', i.day)
        month = query.histroyLoginInfo('month', i.month)
        return jsonify({'day':len(day),'month':len(month)})

    behs = query.histroyLoginInfo(paras1,paras2)
    return jsonify({"count":len(behs)})

#查询user表中有多少用户
@admin.route('/usercount',methods=['POST'])
def userCount():
    return jsonify({'count':query.userCounts()})

# 查询一共剩余多少积分
@admin.route('/allpoints',methods=['POST'])
def allpoints():
    # http是否为post
    if request.method != 'POST':
        return jsonify({status_code.statusCode: status_code.http_type_get})

        # rsa参数是否为空
    value = request.form.get("value")
    if value == None:
        return jsonify({status_code.statusCode: status_code.valueRSAIsWrong})

        # 解密成string
    decodeStr = decryption(value)
    # jsonn --> dictt
    value_dict = json.loads(decodeStr)
    print "admin uuid :",value_dict["uuid"]
    points = query.allPoints()
    return jsonify({"count":points})

####################################################################
#添加表model 后调用增加表
@admin.route('/addtable')
def addTable():
    init_db()
    return "addTable"

#更新公私钥
@admin.route('/updatersakey')
def updateRSAKey():
    rsaCipher.masterKeyPair()
    rsaCipher.ghostKeyPair()

@admin.route('/test')
def test():

    print  query.test()
    return jsonify({'a':'b'})


#查询某一天 某个月 某年 的登录信息
@admin.route('/historylogin',methods=['GET'])
def historylogin():
    # print query.historyForLoginTime()
    print query.historyForCurrentDay()
    return jsonify({'status': 1})

#查询所有用户的总积分
#了解当前用户的积分情况，做数据分析
# @admin.route('/allpoints',methods=['GET'])
# def allpoints():
#     print query.allPoints()
#     return jsonify({'status':1})


@admin.route('/order',methods=['GET'])
def order():
    deal_Prce = int(random.uniform(10, 20))
    goods_name = 'fruit'
    flag = sqlmodel.addOrder(deal_Prce, goods_name)
    return jsonify({'status':deal_Prce})

# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@admin.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
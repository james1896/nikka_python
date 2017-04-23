# -*- coding: utf-8 -*-

import random
from . import admin
from flask import jsonify
from app.config import init_db
from ..templates import sqlmodel
from app.config import db_session

from app.venv.rsa import rsaCipher

from ..venv.mysql import query



#这里要注意是admin.route (即对应蓝图的名称)
@admin.route('/')
def index():
    return "hello admin"

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
@admin.route('/allpoints',methods=['GET'])
def allpoints():
    print query.allPoints()
    return jsonify({'status':1})


#查询user表中有多少用户
@admin.route('/userCount')
def userCount():
    return jsonify({'data':query.userCounts()})


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
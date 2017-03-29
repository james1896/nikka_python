# -*- coding: utf-8 -*-

import random
from . import admin
from flask import jsonify
from ..templates import sqlmodel
from app.config import db_session

from app.venv.rsa import rsaCipher


#这里要注意是admin.route (即对应蓝图的名称)
@admin.route('/')
def index():
    rsaCipher.masterKeyPair()
    rsaCipher.ghostKeyPair()
    return "hello admin"


###########################    order For Master    #############################################

@admin.route('/historylogin',methods=['GET'])
def historylogin():
    print sqlmodel.historyForLoginTime()
    return jsonify({'status': 1})

@admin.route('/allpoints',methods=['GET'])
def allpoints():
    print sqlmodel.allPoints()
    return jsonify({'status':1})


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
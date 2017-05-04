# -*- coding: UTF-8 -*-
from flask import jsonify

from app import db_session
from app.venv import cacheRedis
from app.venv.mysql.model import User
from . import views_v1_0
from . import client_v1_1


@client_v1_1.route('/test1')
def test1():
    try:
        user = User.query.filter(User.user_id == 14929000454).first()
        user.points = user.points + 1
        db_session.commit()
        return jsonify({"test1":user.points})
    except:
        return jsonify({'test1':1})

@client_v1_1.route('/test')
def test():
    return jsonify({"test":cacheRedis.objForKey("test")})



@client_v1_1.route('/')
def index():
    return "hello client_v1_1"

@client_v1_1.route('/login', methods=['GET','POST'])
def login():
    view = views_v1_1()
    json = view.login()
    return json





# 初级错误
#第一个  views_v1_0 是模块
#第二个  Views_v1_0  是类
class views_v1_1 (views_v1_0.Views_v1_0):
    def __init__(self):
        views_v1_1.callCount += 1
        print "ViewsV1_1", views_v1_1.callCount



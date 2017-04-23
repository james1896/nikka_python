# -*- coding: UTF-8 -*-
from flask import request, json, jsonify

from app.venv.mysql import query
from app.venv.rsa import rsaCipher
from app.venv.rsa.rsaCipher import random_generator
from . import client_v1_0
from ..venv.error import errorCode

@client_v1_0.route('/')
def index():
    return "hello client_v1_0"

@client_v1_0.route('/login', methods=['GET','POST'])
def login():
    views = Views_v1_0()
    json = views.login()
    return json





class Views_v1_0:

    __callCount = 0

    def __init__(self):
        print "调用父类构造函数"
        Views_v1_0.__callCount += 1
        print "ViewsV1_0", Views_v1_0.__callCount


    def login(self):
        print "login"
        d = self.handlePostData()
        if isinstance(d,dict):
            if d.has_key('username') and d.has_key('password') :
                user = query.login(d['username'], d['password'])
                if user:
                    return jsonify({'status': 1,
                                'user_id': user.user_id,
                                'data': {'points': user.points}})
        else:
            return jsonify(errorCode.parameterError())


    def config(self):
        print "config"

    def handlePostData(self):
        if request.method == 'POST':
            # 得到前端 post 过来的 json字符串
            # data = json.dumps(request.form.get('value'))
            # data为字典类型
            value = rsaCipher.decryptionWithString(request.form.get('value'), random_generator)

            # jsonn --> dictt
            dict = json.loads(value)
            return dict
        # else:
        #     return {errorCode.requestethodsError()}
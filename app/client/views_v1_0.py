# -*- coding: UTF-8 -*-
from flask import request, json, jsonify

from app.venv.mysql import query
from app.venv.mysql.model import User
from app.venv.rsa import rsaCipher
from app.venv.rsa.rsaCipher import random_generator

from . import client_v1_0

@client_v1_0.route('/')
def index():
    return "hello client_v1_0"

@client_v1_0.route('/login', methods=['GET','POST'])
def login():
    views = ViewsV1_0()
    json = views.login()
    return json
    # return jsonify({'status': -1})





class ViewsV1_0:

    callCount = 0

    def __init__(self):
        print "调用父类构造函数"
        ViewsV1_0.callCount+= 1
        print "ViewsV1_0", ViewsV1_0.callCount


    def login(self):
        print "login"
        dict = self.handlePostData()
        if dict.has_key('username') and dict.has_key('password'):
            user = query.login(dict['username'], dict['password'])
            if user:
                return jsonify({'status': 1, 'user_id': user.user_id, 'data': {'points': user.points}})
        else:
            return jsonify({"error":"1001"})


    def handlePostData(self):
        if request.method == 'POST':
            # 得到前端 post 过来的 json字符串
            # data = json.dumps(request.form.get('value'))
            # data为字典类型
            value = rsaCipher.decryptionWithString(request.form.get('value'), random_generator)

            # jsonn --> dictt
            dict = json.loads(value)
            return dict
        else:
            return {'status':'0000'}
# -*- coding: utf-8 -*-

import json
from flask import jsonify
from flask import request
from app import app
from app.config import db_session
from app.templates import sqlmodel
from app.venv.rsa import rsaCipher
from app.venv.rsa.rsaCipher import random_generator

from . import client
@client.route('/')
def index():
    return "hello client"


@client.route('/updatetable',methods=['GET'])
def updatetable():
    # sqlmodel.test()
    return jsonify({'aa':'ss'})

@client.route('/points',methods=['POST'])
def points():
    # if(request.method == 'POST'):
    #     name = request.form['username']
    #     print name
    #     u = sqlmodel.points(name)
    #     print u.pwd
    #     if u:
    #         return jsonify({'points':u.points})
    #     else:
    #         return jsonify({'error':1})
    # return jsonify({'status': 2})
    # name = request.form['username']
    # para = request.form['paras']
    # print 'name:', name, 'para', para
    if request.method == 'POST':
        name = request.form['username']
        para = request.form['paras']
        u = sqlmodel.points(name,para)
        print '积分:',u.points
        if u:
            return jsonify({'points': u.points})
        else:
            return jsonify({'points': 2})
    return jsonify({'points': -1})




@client.route('/users',methods=['GET','POST'])
def users():

    return jsonify({'users':sqlmodel.userCount()})
    # return jsonify({'time':time.time()})

@client.route('/record/<user_id>',methods=['GET','POST'])
def record(user_id):
    # dict = handlePOSTData()
    # if dict.has_key('user_id'):
    #     sqlmodel.record(dict['user_id'])
    sqlmodel.record(user_id)
    return jsonify({'status':1})




###########################    register    #############################################


@client.route('/register',methods=['POST'])
def register():
    dict = handlePOSTData()
    if dict.has_key('username') and dict.has_key('password'):
        user = sqlmodel.register(dict['username'],dict['password'])
        if user:
            return jsonify({'status':1,'user_id':user.user_id})
    return jsonify({'status':2})
###########################    login    #############################################


@client.route('/login',methods=['POST'])
def login():
    # if request.method == 'POST':
    #     name = RSACipher.decryptionWithString(request.form['username'],random_generator)
    #     pwd  = RSACipher.decryptionWithString(request.form['password'],random_generator)
    #
    #     user = sqlmodel.login(name,pwd)
    #     if user:
    #         return jsonify({'status':1,'data':{'points':user.points}})
    dict = handlePOSTData()
    if dict.has_key('username') and dict.has_key('password'):
        user = sqlmodel.login(dict['username'],dict['password'])
        if user:
            return jsonify({'status':1,'user_id':user.user_id,'data':{'points':user.points}})
    return jsonify({'status':2})


############################    test    #############################################


@client.route('/test',methods=['GET','POST'])
def test():
    # m2 = hashlib.md5()
    # m2.update('hello')
    # print m2.hexdigest()
    # return m2.hexdigest()
    # if request.method == 'POST':
        # value = RSACipher.decryptionWithString(request.form.get('value'),random_generator)
        # #得到前端 post 过来的 json字符串
        # # data = json.dumps(request.form.get('value'))
        # #data为字典类型
        # dict = json.loads(value)
        dict = handlePOSTData()
        if dict.has_key('a'):
            print dict['a']
        return jsonify(dict)

def handlePOSTData():
    if request.method == 'POST':
        # 得到前端 post 过来的 json字符串
        # data = json.dumps(request.form.get('value'))
        # data为字典类型
        value = rsaCipher.decryptionWithString(request.form.get('value'), random_generator)
        dict = json.loads(value)
        return dict

@client.route('/updatersakeypairs')
def updateRsaKeypairs():
    rsaCipher.masterKeyPair()
    return jsonify({'status':"ok"})

@app.route('/add/<name>/<pwd>')
def add(name, pwd):
    # encryption = encryptionWithString('hello')
    # print 'random:',random_generator
    # print decryptionWithString(encryption,random_generator)

    # signature = signatureWithString('text')
    # print 'verification:',verificationSignature('text1',signature)
    u = sqlmodel.User(name=name,pwd=pwd)
    try:
        db_session.add(u)
        db_session.commit()
    except Exception, e:
        return 'wrong（key repeat）'
    return     'Add %s user successfully' % name

@app.route('/delete/<name>')
def delete(name):
    try:
        user = sqlmodel.User.query.filter(sqlmodel.User.name == name).first()
        db_session.delete(user)
        db_session.commit()
    except Exception, e:
        return 'there isnot %s' % name
    return 'delete'


@app.route('/update/<name>/<email>')
def update(name,email):
    try:
        u = sqlmodel.User.query.filter(sqlmodel.User.name == name).first()
        u.email = email
        # User.update().where(User.name == name).values(email = email)
        db_session.commit()
    except Exception, e:
        return 'update Exception'
    return 'update finish'



@app.route('/interface',methods=['GET','POST'])
def interface():
    tasks = [
        {
            'id': 12,
            'title': u'Buy groceries',
            'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
        {
            'id': 2,
            'title': u'Learn Python',
            'description': u'Need to find a good Python tutorial on the web',
            'done': False
        }
    ]
    return jsonify({'tasks': tasks})


# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@client.teardown_request
def shutdown_session(exception=None):
    db_session.remove()





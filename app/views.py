# -*- coding: utf-8 -*-

import hashlib
from app import app
from templates import sqlmodel
from config import db_session
from templates import RSACipher
from templates.RSACipher import random_generator

from flask import request
from flask import jsonify
from config import engine

from templates import APNs

# @app.route('/pushnotification')
# def pushNotification():
#     APNs.sendPushNotification();
#     return 'sendNotification success'

# @app.route('/deleteTables',methods=['GET','POST'])
# def deletetables():
#     sqlmodel.deleteTables(engine)
#     return 'deleteTables'
#
# @app.route('/createtables',methods=['GET','POST'])
# def createtables():
#     sqlmodel.createTables(engine)
#     return 'createables'

@app.route('/points',methods=['POST'])
def points():
    if(request.method == 'POST'):
        name = request.form['username']
        print name
        u = sqlmodel.points(name)
        print u.pwd
        if u:
            return jsonify({'points':u.points})
        else:
            return jsonify({'error':1})
    return jsonify({'status': 2})

@app.route('/users',methods=['GET','POST'])
def users():
    return jsonify({'users':sqlmodel.userCount()})

@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        name = RSACipher.decryptionWithString(request.form['username'],random_generator)
        pwd  = RSACipher.decryptionWithString(request.form['password'],random_generator)

        user = sqlmodel.login(name,pwd)
        if user:
            return jsonify({'status':1,'data':{'points':user.points}})

    return jsonify({'status':2})

@app.route('/test',methods=['GET','POST'])
def test():

    m2 = hashlib.md5()
    m2.update('hello')
    print m2.hexdigest()
    return m2.hexdigest()
    # if request.method == 'POST':
    #     print request.form['name']
    #     return jsonify({'obj':RSACipher.decryptionWithString(request.form['name'],random_generator)})
    #
    # if request.method == 'GET':
    #     return jsonify({'obj':RSACipher.decryptionWithString(request.args.get('name'),random_generator)})
    #
    # return jsonify({'error':1})


@app.route('/updatersakeypairs')
def updateRsaKeypairs():
    RSACipher.masterKeyPair()
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


# @app.route('/login',methods=['GET','POST'])
# def login():
#     tasks = [
#         {
#             'id': 12,
#             'title': u'Buy groceries',
#             'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#             'done': False
#         },
#         {
#             'id': 2,
#             'title': u'Learn Python',
#             'description': u'Need to find a good Python tutorial on the web',
#             'done': False
#         }
#     ]
#     if request.method == "POST":
#         return  jsonify({'username': request.form['username']})
#
#     if request.method == 'GET':
#         return jsonify({'tasks': tasks})





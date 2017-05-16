# -*- coding: utf-8 -*-

import json,os
from app import app
from . import client
from flask import request
from ..venv.mysql import query
from app.config import db_session
from app.templates import sqlmodel
from app.venv.rsa import rsaCipher
from ..venv.statuscode import status_code
from ..venv.token import tokenHandle
from werkzeug.utils import secure_filename
from app.venv.rsa.rsaCipher import random_generator
from flask import jsonify, Response, send_from_directory

# 用户相关配置
config = {"a":"bb"}

####################    userInfo    ##############################################

# 针对username加密
@client.route('/userinfo',methods=['POST'])
def userinfo():
    # http是否为post
    if request.method != 'POST':
        return jsonify({status_code.statusCode: status_code.http_type_get})


    uuid = request.form.get("uuid")
    device = request.form.get("device")

    # rsa参数是否为空
    value = request.form.get("value")

    if value != None:
        # 解密成string
        decodeStr = decryption(request.form.get('value'))
        # jsonn --> dictt
        value_dict = json.loads(decodeStr)
        return jsonify({status_code.statusCode: query.userinfo(value_dict['username'], uuid, device),"config":config})
    else:
        return jsonify({status_code.statusCode: query.userinfo("", uuid, device),"config":config})


    # # 解密rsa数据后，操作
    # return_json = userinfo_data_handle(value_dict,uuid,device)
    # print "userInfo接口 返回json数据:\n", return_json
    # return return_json


####################    feedback    ##############################################
@client.route('/feedback',methods=['POST'])
def feedback():
    # http是否为post
    if request.method != 'POST':
        return jsonify({status_code.statusCode: status_code.http_type_get})

    userID = request.form.get("user_id")
    content = request.form.get("content")
    if userID == None or content == None:
        return jsonify({status_code.statusCode:status_code.parameter_none})

    # 这里userID需要传入 外键 是否合理？
    return jsonify({status_code.statusCode:query.feedback(1,content)})

####################    积分转赠    ##############################################
# 积分转赠

@client.route('/pointgift/<sponsor>/<received>/<point>', methods=['GET', 'POST'])
def pointgift(sponsor, received, point):
    print query.pointGift(sponsor, received, point)
    return jsonify({'we': 'heihei'})


####################    积分转赠    ##############################################

@client.route('/points', methods=['POST'])
def points():
    if request.method == 'POST':
        name = request.form['username']
        para = request.form['paras']
        u = sqlmodel.points(name, para)
        print '积分:', u.points
        if u:
            return jsonify({'points': u.points})
        else:
            return jsonify({'points': 2})
    return jsonify({'points': -1})


@client.route('/record/<user_id>', methods=['GET', 'POST'])
def record(user_id):
    sqlmodel.record(user_id)
    return jsonify({'status': 1})


###########################    register    #############################################

@client.route('/register', methods=['POST'])
def register():
    # http是否为post
    if request.method != 'POST':
        return jsonify({status_code.statusCode: status_code.http_type_get})

    # rsa参数是否为空
    value = request.form.get("value")
    if value == None:
        return jsonify({status_code.statusCode: status_code.valueRSAIsWrong})

    # 解密成string
    decodeStr = decryption(request.form.get('value'))
    # jsonn --> dictt
    value_dict = json.loads(decodeStr)

    # 解密rsa数据后，操作
    return_json = register_data_handle(value_dict)
    print "register接口 返回json数据:\n", return_json
    return return_json


def register_data_handle(value_dict):
    if isinstance(value_dict,dict):
    # 对key值抛异常处理
        if value_dict.has_key('username') and value_dict.has_key('password'):
            user = query.register(value_dict['username'], value_dict['password'],'')
            if user:
                return jsonify(({'status': status_code.trueCode,
                                'userToken': tokenHandle.getToken(),
                                'data': {'user_id': user.user_id}}))
            else:
                return jsonify({status_code.statusCode:status_code.register_return_null})
        else:
            return jsonify({status_code.statusCode:status_code.parameter_key_wrong})
    else:
        return jsonify({status_code.statusCode:status_code.valueRSAIsWrong})

###########################    login    #############################################


@client.route('/login', methods=['POST'])
def login():
    # http是否为post
    if request.method != 'POST':
        return jsonify({status_code.statusCode: status_code.http_type_get})

    # rsa参数是否为空
    value = request.form.get("value")
    if value == None:
        return jsonify({status_code.statusCode: status_code.valueRSAIsWrong})

    # 解密成string
    decodeStr = decryption(request.form.get('value'))
    # jsonn --> dictt
    value_dict = json.loads(decodeStr)

    # 解密rsa数据后，操作
    return_json = login_data_handle(value_dict)
    print "login接口 返回json数据:\n", return_json
    return return_json

def login_data_handle(value_dict):
    if isinstance(value_dict,dict):
    # 对key值抛异常处理
        if value_dict.has_key('username') and value_dict.has_key('password'):
            user = query.login(value_dict['username'], value_dict['password'],'','')
            if user:
                return_json = {'status': status_code.trueCode,
                                'userToken':tokenHandle.getToken(),
                                'data': {'points': user.points,
                                         'user_id': user.user_id}}

                return jsonify(return_json)
            else:
                return jsonify({status_code.statusCode:status_code.login_return_null})
        else:
            return jsonify({status_code.statusCode:status_code.parameter_key_wrong})
    else:
        return jsonify({status_code.statusCode:status_code.valueRSAIsWrong})

############################    test    #############################################


#带加密的
@client.route('/test',methods=['POST'])
def test():

    # http是否为post
    if request.method != 'POST':
        return jsonify({status_code.statusCode: status_code.http_type_get})

    # rsa参数是否为空
    value = request.form.get("value")
    if value == None:
        return jsonify({status_code.statusCode:status_code.valueRSAIsWrong})

    decodeStr = decryption(request.form.get('value'))
    # jsonn --> dictt
    dict = json.loads(decodeStr)
    return jsonify({'test':dict['aa']})

#不带加密的
@client.route('/test1',methods=["GET",'POST'])
def test1():
    if request.method == 'POST':
        paras = request.form.get('test1')
        return jsonify({'test1':paras})
    else:
        return jsonify({'test1':'test1'})


############################    test    #############################################

def handlePostData():
    handle_http_type()
    # 得到前端 post 过来的 json字符串
    # data = json.dumps(request.form.get('value'))
    # data为字典类型

    # 判断rsa加密的参数 是否为空
    request_value_rsa('value')
    # rsa解密
    value = decryption(request.form.get('value'))
    # jsonn --> dictt
    dict = json.loads(value)
    return dict

def decryption(encode_value):
    return rsaCipher.decryptionWithString(encode_value, random_generator)

# 判断请求类型
def handle_http_type():
    # if request.method == 'POST':
    #     return status_code.http_type_post
    # if request.method == 'GET':
    #     return status_code.http_type_get
    if request.method != 'POST':
        return jsonify({status_code.statusCode:status_code.http_type_get})

# 判断post过来的参数 是否为空
def request_value_rsa(value):
    if request.form.get(value) == None:
        return status_code.valueRSAIsWrong

@client.route('/helloworld')
def helloworld():
    return jsonify({"token":tokenHandle.getToken()})


@client.route('/')
def index():
    return "hello client"




############################    服务器 image     #############################################
############################    服务器 image     #############################################
############################    服务器 image     #############################################

##上传图片到服务器

#####需要请教大神#########
#上传文件到服务器，可能存在安全隐患

#上传图片到根目录下载images文件夹
UPLOAD_FOLDER=r'images'

# 添加指定允许文件类型的范围
ALLOWED_EXTENSIONS=set(['txt','pdf','png','jpg','jpeg','gif'])

#判断上传文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@client.route('/img',methods=['POST'])
def getimg():
    # file = request.files['file']
    # 表示，从request请求的files字典中，
    # 取出file对应的文件。这个文件是一个FileStorage对象

    # request的files属性，files是一个MultiDict的形式，
    # 而里面的每个文件，都是一个FileStorage对象
    file = request.files['file']
    if file and allowed_file(file.filename):
        # 再来看下这个函数的功能，其实他为了保证文件名不会影响到系统，
        # 他就把文件名里面的斜杠和空格，替换成了下划线
        # 这样，就保证了文件只会在当前目录使用，而不会由于路径问题被利用去做其他事情。
        # 所以，在储存文件之前，通过这个函数把文件名先修改一下
        filename = secure_filename(file.filename)

        # 这个文件对象拥有一个函数功能来保存文件，叫做save()
        # 这个文件对象还拥有一个属性来提取文件名，叫做filename
        # file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        file.save(os.path.join(UPLOAD_FOLDER, 'fileName.png'))
        return jsonify({'a':'b'})


#通过图片名 得到某个图片
@client.route('/uploadedfile/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

##下载服务器图片
@client.route('/image/<imageid>')
def getImage(imageid):
    try:
        #根目录imamges文件夹下 {}是匹配的意思
        image = file("images/{}.jpg".format(imageid))
        resp = Response(image, mimetype="image/jpeg")
        return resp
    except Exception,e:
        return jsonify({'error':'error the image path'})

    #第二种方式也可以实现 但是不知道这两种的区别
    # with open('image/' + str(imageid) + '.jpg') as f:
    #     return Response(f.read(), mimetype='image/jpeg')



###########################################################################################
###########################################################################################
###########################################################################################



##############################       怀旧      #############################################


@app.route('/add/<name>/<pwd>')
def add(name, pwd):
    # encryption = encryptionWithString('hello')
    # print 'random:',random_generator
    # print decryptionWithString(encryption,random_generator)

    # signature = signatureWithString('text')
    # print 'verification:',verificationSignature('text1',signature)
    u = sqlmodel.User(name=name, pwd=pwd)
    try:
        db_session.add(u)
        db_session.commit()
    except Exception, e:
        return 'wrong（key repeat）'
    return 'Add %s user successfully' % name


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
def update(name, email):
    try:
        u = sqlmodel.User.query.filter(sqlmodel.User.name == name).first()
        u.email = email
        # User.update().where(User.name == name).values(email = email)
        db_session.commit()
    except Exception, e:
        return 'update Exception'
    return 'update finish'


@app.route('/interface', methods=['GET', 'POST'])
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

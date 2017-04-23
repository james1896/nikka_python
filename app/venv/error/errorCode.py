# -*- coding: utf-8 -*-

# 1001      注册用户名重复
# 1005      参数错误
# 1010      请求方式错误  有些请求区分 GET POST



def parameterError():
    return {'errorCode':1005}

def requestethodsError():
    return {"errorCode":1010}

def registeUsernameRepeat():
    return {'errorCode':1001}
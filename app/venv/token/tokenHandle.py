# -*- coding: utf-8 -*-

import datetime
import hashlib

def getToken():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    # 生成token
    now_date = datetime.datetime.now()
    print 'now_date', now_date

    # hash对象
    hash_token = hashlib.md5()

    # token字符串
    # token = "flask中文论坛" +\
    #         str(now_date.year) +\
    #         str(now_date.month) + \
    #         str(now_date.day) +\
    #         str(now_date.hour) + \
    #         str(now_date.minute)

    token = "flask中文论坛" + \
            str(now_date.year) + \
            str(now_date.month) + \
            str(now_date.day) + \
            str(now_date.hour)

    # print 'token', token
    hash_token.update(token.encode('utf-8'))
    # 获得加密串
    token = hash_token.hexdigest()
    # print 'tokenHandle: ', token
    return token
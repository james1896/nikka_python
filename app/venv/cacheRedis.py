# -*- coding: utf-8 -*-
import redis

r = redis.Redis(host='127.0.0.1', port=6379)
# r.set('foo', 'Bar')
# print (r.get('foo'))
# r.set('basket','basketball')
# 看信息
info = r.info()

print '\ndbsize: %s' % r.dbsize()
# 看连接
print "ping %s" % r.ping()

def setObject(key,obj):
    r.set(key,obj)

def objForKey(key):
    return r.get(key)


# -*- coding: utf-8 -*-
import atexit
import datetime
from apscheduler.triggers.interval import IntervalTrigger
from app.config import db_session
from apscheduler.schedulers.background import BackgroundScheduler
from app.venv.mysql.model import User


# 实例化BackgroundSchedule对象
scheduler = BackgroundScheduler()
scheduler.start()

# 定义一个定时执行的函数，这个定时执行的函数将会将 某个数据更改
def add_points():
    user = User.query.filter(User.user_id == 14929000454).first()
    print "原来的 points :" ,user.points
    user.points += 1
    db_session.commit()
    now = str(datetime.datetime.now())
    print "add_points: ",user.points
    print

# 接下来定义一个间隔n长时间循环执行任务
scheduler.add_job(
    func            = add_points,
    trigger         = IntervalTrigger(seconds = 5),
    id              ='add_points',
    replace_existing=True)


atexit.register(lambda:scheduler.shutdown())
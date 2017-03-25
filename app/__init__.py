# -*- coding: utf-8 -*-

from flask import Flask
from config import init_db

app = Flask(__name__)



@app.route('/')
def index():
    #初始化数据库（如果没有旧创建 ，如果有就忽略）
    init_db()
    return 'Nikka/ app'


if __name__ == '__main__':
    init_db()

from app import views
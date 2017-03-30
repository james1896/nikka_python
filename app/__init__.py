# -*- coding: utf-8 -*-

from flask import Flask

from app.config import init_db

app = Flask(__name__)

from .admin import admin as admin_blurprint
from .client import client as  client_blurprint


#   注册蓝图
#   url_prefix是访问这个蓝图根目录的链接前缀
#   像这里把admin作为链接的前缀，要访问 admin视图文件的根目录的话就是  www.abc.com/admin
app.register_blueprint(admin_blurprint,url_prefix='/admin')
app.register_blueprint(client_blurprint,url_prefix='/client')



@app.route('/')
def index():
    #初始化数据库（如果没有旧创建 ，如果有就忽略）

    return 'Nikka/ app'


# if __name__ == '__main__':
#     print 'main'
#     init_db()

from app.client import views
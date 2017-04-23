# -*- coding: utf-8 -*-

from flask import Flask

from app.config import init_db
from app.config import db_session

app = Flask(__name__)

from .admin import admin as admin_blurprint
from .client import client as  client_blurprint
from .client import client_v1_0 as  client_v1_0_blurprint
from .client import client_v1_1 as  client_v1_1_blurprint


#   注册蓝图
#   url_prefix是访问这个蓝图根目录的链接前缀
#   像这里把admin作为链接的前缀，要访问 admin视图文件的根目录的话就是  www.abc.com/admin
app.register_blueprint(admin_blurprint,url_prefix='/admin')

app.register_blueprint(client_blurprint,url_prefix='/client')
app.register_blueprint(client_v1_0_blurprint,url_prefix='/client_v1_0')
app.register_blueprint(client_v1_1_blurprint,url_prefix='/client_v1_1')



@app.route('/')
def index():
    #初始化数据库（如果没有旧创建 ，如果有就忽略）

    return 'Nikka/ app'


# if __name__ == '__main__':
#     print 'main'
#     init_db()

from app.client import views



# 在您的应用当中以一个显式调用 SQLAlchemy , 您只需要将如下代码放置在您应用的模块中。
# Flask 将会在请求结束时自动移除数据库会话:
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
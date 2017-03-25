# -*- coding: utf-8 -*-
from MySQLdb.constants.REFRESH import LOG
from sqlalchemy import Boolean, Float,ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import Table
from config import Base, db_session

import time






def addItem(name,email):
    u = User(name=name, email=email)
    try:
        db_session.add(u)
        db_session.commit()
    except Exception, e:
        return 'wrong（key repeat）'
    return 'Add %s user successfully' % name

def record(user_id):
    try:
        order = Order.query.filter(Order.user_id == user_id).all()
        print 'orderdsafda:',len(order)
    except Exception, e:
        return 'there isnot %s'
    return order

def addOrder(deal_time,deal_Prce,goods_name):
    user_id = 1
    order = Order(user_id=user_id,deal_time=deal_time,deal_Prce=deal_Prce,goods_name=goods_name)
    try:
        db_session.add(order)
        db_session.commit()
    except Exception,e:
        return 0
    return 1
#更新积分接口

#如果paras ＝ 0 表示查询当前积分
#如果paras > 0 表示更改当前积分
def points(name,paras):
    if int(paras) == 0:
        try:
            u = User.query.filter(User.name == name).first()
            print 'userName:',u.name,'积分',u.points
        except Exception, e:
            return 'there isnot %s' % name
        return u

    if int(paras) > 0:
        try:
            u = User.query.filter(User.name == name).first()
            u.points = paras
            db_session.commit()
        except Exception, e:
            return 'there isnot %s' % name
        return u

#注册接口
#
def register(name,pwd):
    # user_id = ticks%10000*100000*1000+1*1000
    u = User(name = name, pwd= pwd,user_id=int(time.time()))
    try:
        db_session.add(u)
        db_session.commit()
        return u
    except Exception,e:
        return None

#登录接口
#
def login(name,pwd):
    try:
        u = User.query.filter(User.name==name).first()
    except Exception, e:
        return 'there isnot %s' % name

    if  u:
        if u.pwd == pwd:
            # points = User.query.filter(User.i==name).first()
            return u
    else:
        return False

##################################################################

#没测试成功
def deleteTables(migrate_engine):
    meta = MetaData(migrate_engine)
    meta.reflect(migrate_engine)

    # table_names = ['compute_node_stats', 'compute_nodes', 'instance_actions',
    #                'instance_actions_events', 'instance_faults', 'migrations']
    table_names = ['user']
    for table_name in table_names:
        # 创建表对象, 然后在通过表对象来调用 drop() 方法实现删除.
        table = Table('dump_' + table_name, meta)
        table.drop(checkfirst=True)


#添加一张或者多张表
def define_tables(meta):
    # 定义一个 Table 对象
    new_table_name = Table(
        "user", meta,
        Column("created_at", DateTime),
        Column("updated_at", DateTime),
        Column("deleted_at", DateTime),
        Column("deleted", Boolean),
        mysql_engine="InnoDB")
    return [new_table_name]

def createTables(migrate_engine):
    try:
        meta = MetaData()
        meta.bind = migrate_engine

        # create all tables
        # Take care on create order for those with FK dependencies
        tables = define_tables(meta)

        # 循环创建表列表
        for table in tables:
            try:
                table.create()
            except Exception:
                print 'upgrade table'
                # LOG.info(_LE('Exception while creating table.'))
                raise
    except Exception,e:
        return e




def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    tables = define_tables(meta)
    tables.reverse()
    for table in tables:
        table.drop()

    # 为数据库添加一张或多张新表
    #
    # 当需要为
    # Openstack
    # 项目新添一张表时, 我们会 / opt / stack / nova / nova / db / sqlalchemy / migrate_repo / versions
    # 目录下新建一个文件, 并且需要为文件名指定一个有序的编号, EG.
    # 016
    # _add_new_table.py
    #
    # from sqlalchemy import Boolean, Column, DateTime, BigInteger
    # from sqlalchemy import MetaData, String, Table
    #
    # from oslo_log import log as logging
    #
    # LOG = logging.getLogger(__name__)
    #
    # def define_tables(meta):
    #     # 定义一个 Table 对象
    #     new_table_name = Table(
    #         "new_table_name", meta,
    #         Column("created_at", DateTime),
    #         Column("updated_at", DateTime),
    #         Column("deleted_at", DateTime),
    #         Column("deleted", Boolean),
    #         mysql_engine="InnoDB")
    #     ...
    #
    #     return [new_table_name, ...]
    #
    # def upgrade(migrate_engine):
    #     meta = MetaData()
    #     meta.bind = migrate_engine
    #
    #     # create all tables
    #     # Take care on create order for those with FK dependencies
    #     tables = define_tables(meta)
    #
    #     # 循环创建表列表
    #     for table in tables:
    #         try:
    #             table.create()
    #         except Exception:
    #             LOG.info(_LE('Exception while creating table.'))
    #             raise
    #
    # def downgrade(migrate_engine):
    #     meta = MetaData()
    #     meta.bind = migrate_engine
    #     tables = define_tables(meta)
    #     tables.reverse()
    #     for table in tables:
    #         table.drop()
    #
    #
    # 删除一张或多张表
    #
    # from sqlalchemy import MetaData
    # from sqlalchemy import Table
    #
    # def upgrade(migrate_engine):
    #     meta = MetaData(migrate_engine)
    #     meta.reflect(migrate_engine)
    #
    #     table_names = ['compute_node_stats', 'compute_nodes', 'instance_actions',
    #                    'instance_actions_events', 'instance_faults', 'migrations']
    #     for table_name in table_names:
    #         # 创建表对象, 然后在通过表对象来调用 drop() 方法实现删除.
    #         table = Table('dump_' + table_name, meta)
    #         table.drop(checkfirst=True)
    #
    #
    # 为旧表添加一个字段
    #
    # from sqlalchemy import Column, MetaData, String, Table
    #
    # NEW_COLUMN_NAME = 'initiator_name'
    #
    # def upgrade(migrate_engine):
    #     meta = MetaData()
    #     meta.bind = migrate_engine
    #
    #     # 定义一个表对象, 因为是更新操作, 所以表 exsi_hypervisors 需要已经存在于数据库中
    #     exsi_hypervisors = Table('exsi_hypervisors', meta, autoload=True)
    #     # 定义一个字段对象
    #     initiator_protocol = Column(NEW_COLUMN_NAME, String(length=255))
    #     # 如果表中还没有该字段, 则添加一个新的字段
    #     if not hasattr(exsi_hypervisors.c, NEW_COLUMN_NAME):
    #         # 表对象调用 create_column() 方法来将字段插入
    #         exsi_hypervisors.create_column(initiator_protocol)
    #
    #
    # 为旧表更新一个字段
    #
    # from sqlalchemy import Column, MetaData, String, Table
    #
    # NEW_COLUMN_NAME = 'initiator_name'
    #
    # def upgrade(migrate_engine):
    #     meta = MetaData()
    #     meta.bind = migrate_engine
    #
    #     # 获取一个表对象
    #     exsi_hypervisors = Table('exsi_hypervisors', meta, autoload=True)
    #
    #     # 如果表对象中已经存在了 metadata_reserve 属性(字段), 则 alter 该属性(字段)
    #     if hasattr(exsi_hypervisors.c, 'metadata_reserve'):
    #         # 获取 metadata_reserve 属性对象
    #         exsi_hypervisors_metadate_reserve = getattr(exsi_hypervisors.c,
    #                                                     'metadata_reserve')
    #         # 通过属性对象来调用 alter() 方法, 并且传入需要更新的字段名和类型作为实参
    #         exsi_hypervisors_metadate_reserve.alter(name='initiator_protocol',
    #                                                 type=String(255))
    #
    #
    # 为旧表初始化一条新的记录
    #
    # from datetime import datetime
    # from uuid import uuid4
    #
    # from sqlalchemy import MetaData, Table
    #
    # def upgrade(migrate_engine):
    #     meta = MetaData()
    #     meta.bind = migrate_engine
    #
    #     # 定义要插入的记录数据
    #     values = [{'created_at': datetime.utcnow(),
    #                'id': str(uuid4()),
    #                'group': 'global',
    #                'setting_option': 'cpu_over_allocate',
    #                'setting_value': '6',
    #                'description': 'Over allocate CPU'}]
    #
    #     # 创建一个 table 对象, 该表必须是已经存在于数据库内的表, 才能够被插入
    #     system_settings = Table('system_settings', meta,
    #                             autoload=True)
    #     # 通过表对象来调用 insert() 方法实现插入数据
    #     for value in values:
    #         system_settings.insert().values(value).execute()
    #
    # def downgrade(migrate_engine):
    #     meta = MetaData()
    #     meta.bind = migrate_engine
    #
    #     system_settings = Table('system_settings', meta,
    #                             autoload=True)
    #     try:
    #         system_settings.delete(). \
    #             where(system_settings.c.setting_option == 'cpu_over_allocate'). \
    #             execute()
    #
    #     except Exception as e:
    #         raise e
    # 最后
    #
    # 在实现了数据库修改的文件之后执行指令:
    #
    # serviceName - manager
    # db
    # dync
    # 1
    # 1
    # 就能够对现有的数据库进行更新.


#查询user表中有多少条数据
def userCount():
    return db_session.query(User).filter_by().count()


#########################   mysql表结构    #####################################################




class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    pwd = Column(String(120), unique=False)
    user_id = Column(Integer, unique=True)
    email = Column(String(120), unique=False)
    points = Column(Float, unique=False)


    def __init__(self, name=None,pwd=None,user_id=None):
        self.name = name
        self.pwd = pwd
        self.user_id = user_id
        self.email = None
        self.points = 0.0


    # def __init__(self, name=None,pwd=None,email=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.email = email
    #
    # def __init__(self, name=None,pwd=None,points=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.points = points

    def __repr__(self):
        return '%s (%r, %r)' % (self.__class__.__name__, self.name, self.email)



class Order(Base):
    __tablename__ = 'orders'

    id          = Column(Integer, primary_key=True)
    order_id    = Column(Integer, unique=True)
    deal_time   = Column(String(120), unique=True)
    deal_Prce   = Column(Float,unique=True)
    goods_name  = Column(String(30),unique=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, user_id=None,deal_time=None,deal_Prce=None,goods_name=None):
        self.user_id = user_id
        self.deal_time = deal_time
        self.deal_Prce = deal_Prce
        self.goods_name = goods_name

        self.order_id = 100000

    # def __init__(self, name=None,pwd=None,email=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.email = email
    #
    # def __init__(self, name=None,pwd=None,points=None):
    #     self.name = name
    #     self.pwd = pwd
    #     self.points = points

    def __repr__(self):
        return '%s (%r, %r)' % (self.__class__.__name__, self.user_id, self.goods_name)

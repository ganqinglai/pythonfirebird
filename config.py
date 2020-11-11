import os
import uuid
import base64
from redis import Redis, ConnectionPool
import fdb
from dbutils.pooled_db import PooledDB
"""
fdbbase = {
    "host": "168.0.0.71",
    "port": 3050,
    "database": r'd:\\python\\python20201013\\MYTORNADO.DB',
    "user": "SYSDBA",
    "password": "masterkey",
    "charset": "UTF8"
}
"""
pool = ConnectionPool(host="168.0.0.71",
                      port=6379,
                      password="123456",
                      decode_responses=True)
redisPool = Redis(connection_pool=pool)

GUID = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
BASE_DIRS = os.path.dirname(__file__)
settings = {
    "template_path": os.path.join(BASE_DIRS, "templates"),
    "static_path": os.path.join(BASE_DIRS, "statics"),
    "cookie_secret": b'ZAVWU9xhSxeEG8+35JjceYA079lD/EQVgvSC3iXU/P8=',  # GUID,
    # "xsrf_cookies": True
}


class Config(object):
    # DEBUG = True
    # SECRET_KEY = "umsuldfsdflskjdf"
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
    # SESSION_REFRESH_EACH_REQUEST= True
    # SESSION_TYPE = "redis"
    PYFDB_POOL = PooledDB(
        creator=fdb,  # 使用链接数据库的模块
        maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],
        # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='168.0.0.71',
        port=3050,
        user='SYSDBA',
        password='masterkey',
        database=r'd:\python\python20201013\MYTORNADO.DB',
        charset='UTF8')


"""
class ProductionConfig(Config):
    SESSION_REDIS = Redis(host='192.168.0.94', port='6379')


class DevelopmentConfig(Config):
    SESSION_REDIS = Redis(host='127.0.0.1', port='6379')


class TestingConfig(Config):
    pass
"""

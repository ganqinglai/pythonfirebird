"""
import tornado.ioloop
from project_settings.db_settings import DBMysql

user = DBMysql[0]["user"]
host = DBMysql[0]["host"]
db = DBMysql[0]["db"]
password = DBMysql[0]["password"]
import tormysql
import pymysql.cursors

pool = tormysql.ConnectionPool(
    # max_connections=100,  # max open connections
    max_connections=500,  # max open connections
    idle_seconds=7500,  # conntion idle timeout time, 0 is not timeout
    wait_connection_timeout=600,  # wait connection timeout
    host=host,
    user=user,
    passwd=password,
    db=db,
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor # 获取的是字典形式， 没有这句获取的是元组
)

from yang_test.common.connect_pool import pool

from yang_test.common.base_model import BaseModel


# class DBBase(BaseModel):
class DBBase():
    def __init__(self, conn=None):
        self.conn = conn

    async def update_data(self, sql):
        # 更新数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
        return ""

    async def get_many(self, sql, n):
        # 获取 多条数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                data = cursor.fetchmany(n)
        # return data
        return BaseModel.query(data)

    async def get_all(self, sql):
        # 获取 所有数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                data = cursor.fetchall()
        return BaseModel.query(data)

    async def get_one(self, sql):
        # 获取一条数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                data = cursor.fetchone()
        return BaseModel.query(data)

    async def add_one(self, sql):
        # 插入一条数据
        flag = True
        async with await pool.Connection() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql)
            except Exception as e:
                await conn.rollback()
                flag = False
            else:
                await conn.commit()
        return flag



class BaseModel(dict):
    _table_name = ''
    _optional_cols = []

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self._optional_cols:
                return ''
            else:
                raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def get_model(cls, data):
        if not data or not len(data):
            return None
        if isinstance(data, list):
            models = [cls(d) for d in data]
            return models

        if isinstance(data, dict):
            return cls(data)
        return None

    @classmethod
    def query(cls, data):
        return cls.get_model(data)

    @classmethod
    def get_model_old(cls, data):
        if not data or not len(data):
            return None
        if isinstance(data, list):
            models = list()
            for d in data:
                m = cls(d)
                models.append(m)
            return models

        if isinstance(data, dict):
            return cls(data)
        return None


from yang_test.db.db_base import DBBase

STATE_DEFAULT = 1


class member(DBBase):
    def __init__(self, conn=None):
       pass

    async def get_by_users(self, user_ids):
        data = dict()
        data["state"] = STATE_DEFAULT
        if not user_ids or (user_ids and len(user_ids) == 1):
            data["user_id"] = user_ids[0] if user_ids else ""
            sql = "SELECT user_id,college_id FROM member where state='{state}' and user_id = '{user_id}'"
        else:
            data["user_id"] = tuple(user_ids)
            sql = "SELECT user_id,college_id FROM member where state='{state}' and user_id in {user_id}"
        sql = sql.format(**data)

        one = await self.get_all(sql)
        return one

    async def get_one_by_user(self, user_id):
        data = dict()
        data["user_id"] = user_id
        data["state"] = STATE_DEFAULT
        sql = "SELECT * FROM member where user_id='{user_id}' and state='{state}' ORDER  BY created_at DESC"
        sql = sql.format(**data)
        one = await self.get_one(sql)
        return one

    async def update_state_by_college(self, college_id, state=0):
        # 修改 动态的状态 默认修改为无效
        data = dict()
        data["college_id"] = college_id
        data["state"] = state
        sql = "UPDATE member SET state = '{state}'  where college_id='{college_id}'"
        sql = sql.format(**data)
        res = await self.update_data(sql)
        return True


     @classmethod
    async def get_10(cls):
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                data = dict()
                data["state"] = 1
                data["approval_state"] = 3
                data["parent_id"] = "NULL"
                dd = ["4eb1c040f14111e8870c509a4c9436be", "d5fe1550f13a11e8ab55509a4c9436be"]
                data["situation_id"] = tuple(dd)
                # sql = "SELECT id,created_at,content FROM comment where  state={state} and approval_state !='{approval_state}' and parent_id IS NULL and situation_id in {situation_id}"
                sql = "SELECT id,created_at,content FROM comment where  state={state} and approval_state !='{approval_state}' and parent_id IS {parent_id} and situation_id in {situation_id}"
                # sql = "SELECT id,created_at,content FROM comment WHERE parent_id is NULL "
                sql = sql.format(**data)

                await cursor.execute(sql)
                data = cursor.fetchall()

        return data

    @classmethod
    async def get(cls):
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                # data = dict()
                # data["db_name"] = "configuration"
                # data["timestamp"] = "timestamp"
                # data["identity"] = "identity"
                # sql = "SELECT {timestamp},{identity} FROM {db_name} "
                # sql = sql.format(**data)
                # await cursor.execute(sql)
                # data = cursor.fetchone()

                data = dict()
                data["db_name"] = "configuration"
                data["aa"] = "timestamp" + "," + "identity"
                # field_list = ["timestamp", "identity"] # ok
                # field_list = ["*"] # ok
                field_list = ["timestamp as tt", "identity"]  # ok
                field_list = ["sum(threshold) as thr"]  # ok 可以有哈哈
                field_list = ["identity", "threshold"]  # ok 可以有哈哈
                data["field"] = ",".join(field_list)
                # condition = "threshold >100"  # 可行
                condition = "threshold >100 order by threshold desc"  # 可行 perfect
                condition = "id in(1,3,4)"  # ok
                condition = "description in('信誉积分下限')"  # 真棒
                # ======
                # ids = [1, 3, 5]
                # ids = tuple(ids)
                # condition = "id in {ids}".format(ids=ids)  # 真棒
                ###======= 可行
                # a = 1, 2, 3  # 这种可以
                a = [1, 3, 5]

                # ids = [1]
                # ids = ",".join(ids)
                # ids = tuple(ids)
                # ids = (1)  # 这个不可以
                # condition = "id in {ids}".format(ids=ids)  # 真棒
                # condition = "id in (1)"  # 真棒 这个可以
                # condition = "id in {ids}".format(ids=ids)  # 真棒 这个可以
                # condition = "id in {ids}".format(ids=a)  # 真棒 这个可以
                def get_in_data(data_):
                    if isinstance(data_, list):
                        if len(data_) > 1:
                            data_ = tuple(data_)
                        elif len(data_) == 1:
                            data_ = "(" + str(data_[0]) + ")"
                    return data_

                # ids = [1, 3, 5]
                ids = [1]
                ids = get_in_data(ids)
                # ids = tuple(ids)
                condition = "id in {ids}".format(ids=ids)  # 真棒 这个可以
                data["condition"] = condition
                # sql = "SELECT {field} FROM {db_name} WHERE {condition}"
                sql = "SELECT {field} FROM {db_name} WHERE {condition}"
                sql = sql.format(**data)
                await cursor.execute(sql)
                data = cursor.fetchall()
                # data = cursor.fetchone()
        return data


@classmethod
    async def update_data(cls):
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                db_name = "school"
                set_data = dict()
                set_data["name"] = "你知道的"
                set_field = "name='{name}'"
                set_field = set_field.format(**set_data)
                condition = "id = '2b65e14c-10cd-11e9-b36b-509a4c9436be'"
                data = dict()
                data["db_name"] = db_name
                data["set_field"] = set_field
                data["condition"] = condition
                sql = "UPDATE {db_name} SET {set_field}  where {condition}"

                sql = sql.format(**data)
                await cursor.execute(sql)
        return

 @classmethod
    async def add_new(cls):
        async with await pool.Connection() as conn:
            flag = True
            try:
                async with conn.cursor() as cursor:
                    c1 = uuid.uuid1()
                    # c1 = "op"
                    data_ = dict()
                    data_["id"] = str(c1) # 不加str() 在这个列表里会报错
                    data_["name"] = "湖北 hello"
                    data = dict()
                    # field = "id, name"

                    data["field"] = ",".join(list(data_.keys()))
                    values = ["'" + str(d) + "'" for d in data_.values()]
                    data["values"] = ",".join(values)
                    data["db_name"] = "school"
                    # sql = "INSERT INTO school({field}) VALUES('{id}', '{name}')".format(**data)  # 可以的
                    # sql = "INSERT INTO school({field}) VALUES({values})".format(**data)  #
                    sql = "INSERT INTO {db_name}({field}) VALUES({values})".format(**data)  #
                    await cursor.execute(sql)
            except Exception as e:
                await conn.rollback()
                flag = False
            else:
                await conn.commit()

        return flag


   @classmethod
    async def delete_some(cls):
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                data = dict()
                data["db_name"] = "school"
                data["condition"] = "id='819df450-197e-11e9-991e-509a4c9436be'"
                sql = "delete from {db_name} WHERE {condition}".format(**data)
                await cursor.execute(sql)

        return ""


from yang_test.common.connect_pool import pool
from yang_test.common.base_model import BaseModel


# class DBBase(BaseModel):
class DBBase():
    def __init__(self, conn=None, db_name=None):
        self.conn = conn
        self.db_name = db_name

    def get_delete_sql(self, condition=None):
        # 获取删除的sql
        # :param condition: 删除的条件 （字符串）
        # :return: 返回删除语句
        data = dict()
        data["db_name"] = self.db_name
        if condition:
            data["condition"] = condition
            sql = "delete from {db_name} WHERE {condition}".format(**data)
        else:
            sql = "delete from {db_name}".format(**data)
        return sql

    def get_add_sql(self, data=None):
        # 获取添加sql
        # :param data: 字典类型数据 （dict）
        # :return:

        if not data:
            return False
        data_data = dict()
        data_data["db_name"] = self.db_name
        data_data["fields"] = ",".join(list(data.keys()))
        values = ["'" + str(d) + "'" for d in data.values()]
        data_data["values"] = ",".join(values)
        sql = "INSERT INTO {db_name}({field}) VALUES({values})".format(**data)
        return sql

    def get_update_sql(self, set_field=None, condition=None):

        # 获取更新 数据的sql
        # :param set_field: 要设置的字段 （字符串）
        # :param condition: 判断的条件 （字符串）
        # :return: 返回 return

        if not set_field:
            return False
        data = dict()
        data["db_name"] = self.db_name
        data["set_field"] = set_field
        if condition:
            data["condition"] = condition
            sql = "UPDATE {db_name} SET {set_field}  where {condition}"
        else:
            sql = "UPDATE {db_name} SET {set_field}"

        sql = sql.format(**data)
        return sql

    def get_select_sql(self, field_list=None, condition=None):

        # 获得查询sql
        # 传入field_list 必须为list 列表
        # :param db_name: 数据库的名字 （字符串）
        # :param condition: 条件语句 字符串 （字符串）
        # :param field_list: 字段列表， 操作动作想要的字段 （列表）
        # :return:

        field = ",".join(field_list) if field_list else "*"
        data = dict()
        data["field"] = field
        data["db_name"] = self.db_name
        if condition:
            data["condition"] = condition
            sql = "SELECT {field} FROM {db_name} WHERE {condition}"
        else:
            sql = "SELECT {field} FROM {db_name}"
        sql = sql.format(**data)
        return sql

    def get_in_data(self, data_):
        # 为了解决 条件中有 in 的情况 拼接in 中数据的时候
        # 当列表 为一个的时候 tuple() 会是（1,）的效果， 在in 语句中会出错的
        # 这个方法就是为了 让拼接者不去考虑处理逻辑直接传入 一个列表 就可以不管是 长度是1 还是大于1

        if isinstance(data_, list):
            if len(data_) > 1:
                data_ = tuple(data_)
            elif len(data_) == 1:
                data_ = "(" + str(data_[0]) + ")"
        return data_

    async def update_data(self, sql):
        # 更新数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
        return ""

    async def get_many(self, sql, n):
        # 获取 多条数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                data = cursor.fetchmany(n)
        # return data
        return BaseModel.query(data)

    async def get_all(self, sql):
        # 获取 所有数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                data = cursor.fetchall()
        return BaseModel.query(data)

    async def delete_data(self, sql):
        # 删除
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
        return ""

    async def get_one(self, sql):
        # 获取一条数据
        async with await pool.Connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql)
                data = cursor.fetchone()
        return BaseModel.query(data)

    async def add_one(self, sql):
        # 插入一条数据
        flag = True
        async with await pool.Connection() as conn:
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql)
            except Exception as e:

                await conn.rollback()
                flag = False
            else:
                await conn.commit()
        return flag


DB_NAME = "club_member"


class ClubMember(DBBase):
    def __init__(self):
        super(ClubMember, self).__init__(conn=conn, db_name=DB_NAME)

    async def get_one_by_user(self, user_id):
        field = ["*"] # 想需要的字段列表， eg:field_list = ["sum(threshold) as thr"],field_list = ["identity", "threshold"]
        data = dict()
        data["user_id"] = user_id
        data["state"] = STATE_DEFAULT
        condition = "user_id='{user_id}' and state='{state}' order by created_at desc"
        condition = condition.format(**data) # 拼接的where后面的条件字符串语句
        sql = self.get_select_sql(field, condition)       
        one = await self.get_one(sql)
        return one
"""

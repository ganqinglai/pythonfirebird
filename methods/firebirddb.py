from config import Config


class FdbObj():
    @staticmethod
    def open():
        POOL = Config.PYFDB_POOL
        conn = POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_one(cls, sql):
        conn, cursor = cls.open()
        cursor.execute(sql)
        obj = cursor.fetchone()
        cls.close(conn, cursor)
        return obj

    @classmethod
    def fetch_all(cls, sql):
        conn, cursor = cls.open()
        cursor.execute(sql)
        obj = cursor.fetchall()
        cls.close(conn, cursor)
        return obj

    @classmethod
    def insert_czy(cls, sql):
        conn, cursor = cls.open()
        obj = cursor.execute(sql)
        conn.commit()
        cls.close(conn, cursor)
        return obj

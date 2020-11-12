import tornado.web
from tornado.httpclient import AsyncHTTPClient
# import methods.readdb as mrd
from methods.firebirddb import FdbObj
from .base import BaseHandler
import json
from config import redisPool
# from tornado import gen


class LoginHandler(BaseHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            code = 500
            # 返回500界面
            self.write({"codeid": code, "msg": "服务器内部错误"})
        elif status_code == 400:
            code = 400
            # 返回404界面
            self.write({"codeid": code, "msg": "请注册用户信息"})
        self.set_status(code)

    def get(self):
        usernames = FdbObj.fetch_all('select username,pwd from czy')
        one_user = usernames[0][0]
        pwd = usernames[0][1]
        rjsonarr = json.dumps({"user": one_user, "pwd": pwd})
        self.write(rjsonarr)

    def post(self):
        # print(self.request.headers)
        jsonheaders = json.loads(json.dumps(dict(self.request.headers)))
<<<<<<< HEAD
        # print(jsonheaders)
        # print("-------------------")
        print(jsonheaders.get("User-Agent"))
        # print("-------------------")
=======
        print(jsonheaders)
        print("-------------------")
        print(jsonheaders.get("User-Agent"))
        print("-------------------")
>>>>>>> 37a28c10304c011320c1db8e129d46ff1b5cf7f1
        print(self.get_secure_cookie("visencookie"))
        jsonbody = dict(json.loads(self.request.body))
        username = jsonbody.get("username")
        if not redisPool.hexists(name="czy", key=username):
            sql = "select username,pwd from czy where username='%s'" % username
            user_infos = FdbObj.fetch_all(sql)
            if user_infos:
                usermc = user_infos[0][0]
                password = user_infos[0][1]
                redisPool.hset("czy", usermc, password)
                rjsonarr = json.dumps({
                    "usr": usermc,
                    "pwd": password,
                    "type": 0
                })
                return self.write(rjsonarr)
            else:
                """
                password = username
                sql = "insert into czy(username,pwd) values('%s','%s')" % (
                    username, password)
                rbool = FdbObj.insert_czy(sql)
                if rbool:
                    redisPool.hset("czy", username, password)

                rjsonarr = json.dumps({
                    "usr": username,
                    "pwd": password,
                    "type": 1
                })
                return self.write(rjsonarr)
                """
                self.send_error(400)
        else:
            password = redisPool.hget("czy", username)
            rjsonarr = json.dumps({
                "usr": username,
                "pwd": password,
                "type": 2
            })
            return self.write(rjsonarr)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class ErrorHandler(BaseHandler):
    def get(self):
        self.render("error.html")


class Showstudent4(BaseHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            code = 500
            # 返回500界面
            self.write({"codeid": code, "msg": "服务器内部错误"})
        elif status_code == 400:
            code = 400
            # 返回404界面
            self.write({"codeid": code, "msg": "请注册用户信息"})
        self.set_status(code)

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        res = yield self.getDate()
        self.write(res)

    @tornado.gen.coroutine
    def getDate(self):
        url = "https://market.douban.com/categories/?name=classic"  # 请求的服务器
        client = AsyncHTTPClient()  # 创建客户端
        res = yield client.fetch(url)  # 发起请求,请求成功，执行回调函数。
        # client.fetch()执行一个请求，异步返回一个“HTTPResponse”
        if res.error:
            self.send_error(500)
        else:
            data = (res.body)
            # 如果需要将数据转化为json字符串 data = json.loads(res.body)
            raise tornado.gen.Return(
                data
            )  # 类似生成器中 .send,将值data传回 res=yield self.getDate() 即res=data

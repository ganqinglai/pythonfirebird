from tornado.websocket import WebSocketHandler  # socket聊天室


class Chathandler1(WebSocketHandler):
    users = []  # 存放连接信息

    def open(self):  # 当一个WebSocket连接建立后会被服务端调用
        self.users.append(self)
        for user in self.users:
            # 向每一个人发送消息
            print(self.request.remote_ip)
            user.write_message("欢迎{}进入房间".format(self.request.remote_ip))
        # write_message()主动向客服端发送message消息，message可以使字符串挥着字典（自动转为json字符串）

    def on_message(self, message):
        pass

    def on_close(self):
        pass

    def check_origin(self, origin):
        return True

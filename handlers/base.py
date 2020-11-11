import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("visen", "visen")
        self.set_secure_cookie("visencookie", "visen")
        self.set_header("Content-Type", "applictions/json;charset=UTF-8")

    def get_current_user(self):
        return self.get_secure_cookie("user")

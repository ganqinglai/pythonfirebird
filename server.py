import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import tornado.httpserver
from url import url
from config import settings
import platform

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

define("port", default=8083, help="run on the given port", type=int)
define("address", default="168.0.0.71", type=str)

application = tornado.web.Application(handlers=url, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port, options.address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

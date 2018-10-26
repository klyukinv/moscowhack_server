import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import os.path
import json

import constants

define("port", default=8888, help="run on the given port", type=int)


# define("host", default="0.0.0.0") ##localhost now

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (constants.root_link, RootHandler),
            (constants.api_link, APIHandler),
            (constants.connect_link, ConnectHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass


class RootHandler(BaseHandler):
    async def get(self):
        self.render(constants.index_page, github_link=constants.github_link, api_link=constants.api_link,
                    contact_email=constants.contact_email)


class APIHandler(BaseHandler):
    async def get(self):
        self.render(constants.api_page, github_link=constants.github_link, api_link=constants.api_link,
                    contact_email=constants.contact_email)


class ConnectHandler(BaseHandler):
    async def get(self):
        self.render(constants.empty_page, response=str(json.dumps({"connect_status": "OK"}, ensure_ascii=False)))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

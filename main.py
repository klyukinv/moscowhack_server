import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import os.path
import json

import constants
import generator
import user
import init


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (constants.root_link, RootHandler),
            (constants.api_link, APIHandler),
            (constants.connect_link, ConnectHandler),
            (constants.login_link, LoginHandler)
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


class LoginHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            slug = json.loads(slug)
            if not slug['username'] or not slug['password']:
                raise Exception("bad slug")
        except:
            self.render(constants.fail_connect)
            return
        if slug['username'] in user.users and user.users[slug['username']].check_password(slug['password']):
            self.render(constants.empty_page,
                        response=str(
                            json.dumps({"session_id": user.users[slug['username']].session_id}, ensure_ascii=False)))
        else:
            self.render(constants.empty_page, response=str(json.dumps({"connect_status": "FAIL"}, ensure_ascii=False)))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

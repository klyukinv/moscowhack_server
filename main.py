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
from model.healthtest import int_to_sym, int_to_dis


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (constants.root_link, RootHandler),
            (constants.api_link, APIHandler),
            (constants.connect_link, ConnectHandler),
            (constants.login_link, LoginHandler),
            (constants.start_health_test_link, StartHealthTestHandler),
            (constants.health_test_get_question_link, GetQuestionHandler),
            (constants.health_test_post_answer_link, PostAnswerHandler),
            (constants.health_test_results_link, GetResultsHandler)
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
        self.render(constants.empty_page, response=str(json.dumps({"connect_status": "OK"})))


class LoginHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            slug = json.loads(slug)
            if 'username' not in slug or 'password' not in slug:
                raise Exception("bad slug")
        except:
            self.render(constants.fail_connect)
            return
        if slug['username'] in user.users and user.users[slug['username']].check_password(slug['password']):
            self.render(constants.empty_page,
                        response=str(
                            json.dumps({"session_id": user.users[slug['username']].session_id})))
        else:
            self.render(constants.fail_connect)


class StartHealthTestHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            slug = json.loads(slug)
            if 'username' not in slug or 'session_id' not in slug:
                raise Exception("bad slug")
        except:
            self.render(constants.fail_connect)
            return
        if slug['username'] in user.users and user.users[slug['username']].session_id == slug['session_id']:
            _response = user.users[slug['username']].add_test()
            self.render(constants.empty_page,
                        response=str(
                            json.dumps({"test_id": _response})))
        else:
            self.render(constants.fail_connect)


class GetQuestionHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            slug = json.loads(slug)
            if 'username' not in slug or 'session_id' not in slug or \
                    'test_id' not in slug or 'question_number' not in slug:
                raise Exception("bad slug")
        except:
            self.render(constants.fail_connect)
            return
        if slug['username'] in user.users and user.users[slug['username']].session_id == slug['session_id'] and slug[
            'test_id'] in user.users[slug['username']].tests:

            if user.users[slug['username']].tests[slug['test_id']].diagnosis is not None:
                self.render(constants.empty_page,
                            response=str(
                                json.dumps({"diagnosis": user.users[slug['username']].tests[slug['test_id']].diagnosis},
                                           ensure_ascii=False)))
                return

            _buf = user.users[slug['username']].tests[slug['test_id']].get_question()
            if 'diagnosis' in _buf:
                user.users[slug['username']].tests[slug['test_id']].diagnosis = _buf['diagnosis']
                self.render(constants.empty_page,
                            response=str(
                                json.dumps({"diagnosis": int_to_dis(_buf['diagnosis']), "doctor": _buf['doctor']})))
                return

            _response = int_to_sym(_buf['symptom'])
            self.render(constants.empty_page,
                        response=str(
                            json.dumps({"question": _response})))
        else:
            self.render(constants.fail_connect)


class PostAnswerHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            slug = json.loads(slug)
            if 'username' not in slug or 'session_id' not in slug or \
                    'test_id' not in slug or 'question_number' not in slug or 'response' not in slug:
                raise Exception("bad slug")
        except:
            self.render(constants.fail_connect)
            return
        if slug['username'] in user.users and user.users[slug['username']].session_id == slug['session_id'] and \
                slug['test_id'] in user.users[slug['username']].tests:
            # TODO _response = user.users[slug['username']].add_test()

            if user.users[slug['username']].tests[slug['test_id']].diagnosis is not None:
                self.render(constants.empty_page,
                            response=str(
                                json.dumps({"diagnosis": user.users[slug['username']].tests[slug['test_id']].diagnosis},
                                           ensure_ascii=False)))
                return

            _buf = user.users[slug['username']].tests[slug['test_id']].get_response(slug['response'])
            if 'diagnosis' in _buf:
                user.users[slug['username']].tests[slug['test_id']].diagnosis = _buf['diagnosis']
                self.render(constants.empty_page,
                            response=str(
                                json.dumps({"diagnosis": int_to_dis(_buf['diagnosis']), "doctor": _buf['doctor']})))
                return
            _response = ""
            self.render(constants.empty_page,
                        response=str(
                            json.dumps({"next_stage": _response})))
        else:
            self.render(constants.fail_connect)


class GetResultsHandler(BaseHandler):
    async def get(self, slug=None):
        try:
            slug = json.loads(slug)
            if 'username' not in slug or 'session_id' not in slug or 'test_id' not in slug:
                raise Exception("bad slug")
        except:
            self.render(constants.fail_connect)
            return
        if slug['username'] in user.users and user.users[slug['username']].session_id == slug['session_id'] and slug[
            'test_id'] in user.users[slug['username']].tests:

            if user.users[slug['username']].tests[slug['test_id']].diagnosis is not None:
                _response = user.users[slug['username']].tests[slug['test_id']].diagnosis
                self.render(constants.empty_page,
                            response=str(
                                json.dumps({"results": int_to_dis(_response)})))
            else:
                self.render(constants.fail_connect)
        else:
            self.render(constants.fail_connect)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

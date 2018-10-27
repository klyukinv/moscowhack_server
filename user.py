import hashlib
import time
import generator
from health_test import HealthTest


class User:
    def __init__(self, login: str = None, password: str = None, tests=None):
        if tests is None:
            self.tests = {}
        self.login = login
        self.password = password
        self.session_id = generator.id_generator()

    def check_password(self, password: str = "") -> bool:
        # TODO : password check
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        if sha_signature == self.password:
            return True
        # time.sleep(5) ## if brute force
        return False

    def add_test(self) -> str:
        test_id = generator.id_generator()
        self.tests[test_id] = HealthTest(test_id)
        return test_id


users = {}
users["ivan.fil@gmail.com"] = User("ivan.fil@gmail.com", hashlib.sha256("123456".encode()).hexdigest())

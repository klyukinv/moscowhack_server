import hashlib
import time
import generator

class User:
    def __init__(self, login: str = None, password: str = None, tests: list = []):
        self.login = login
        self.password = password
        self.tests = tests
        self.session_id = generator.id_generator()

    def check_password(self, password: str = "") -> bool:
        # TODO : normal password check
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        if sha_signature == self.password:
            return True
        # time.sleep(5)
        return False


users = {}
users["ivan.fil@gmail.com"] = User("ivan.fil@gmail.com", hashlib.sha256("123456".encode()).hexdigest(), [])

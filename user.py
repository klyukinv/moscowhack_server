import hashlib
import time


class User:
    def __init__(self, login: str = None, password: str = None, tests: list = []):
        self.login = login
        self.password = password
        self.tests = tests

    def check_password(self, password: str = "") -> bool:
        # TODO : normal password check
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        if sha_signature == self.password:
            return True
        time.sleep(5)
        return False


users = {}
users["123"] = User("123", hashlib.sha256('123'.encode()).hexdigest(), [])

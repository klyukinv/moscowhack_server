class HealthTest:
    def __init__(self, test_id: str = None):
        if test_id is None:
            raise Exception("test id can not be None")
        self.id = test_id

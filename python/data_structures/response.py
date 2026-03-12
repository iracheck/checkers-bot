from data_structures import ResponseType

class Response:
    def __init__(self, type: ResponseType, msg = None):
        self.type = type
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return f"{self.type}"
        else:
            return f"{self.type} {self.msg}"
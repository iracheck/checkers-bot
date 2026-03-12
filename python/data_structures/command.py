from data_structures import CommandType

class Command:
    def __init__(self, type: CommandType, arg1 = None, arg2 = None, arg3 = None):
        self.type = type
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
from queue import Queue

class Sequence:
    
    def __init__(self, size = 32):
        self.commands = Queue(size)
        self.completed = 0
        self.retry_count = 0
        pass
    
    
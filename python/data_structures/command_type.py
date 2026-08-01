from enum import Enum, auto

class CommandType(Enum):
    PING = auto()
    MOVE = auto()
    MAGNET = auto()
    HOME = auto()
    WAIT = auto()
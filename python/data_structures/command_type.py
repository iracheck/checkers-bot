from enum import Enum, auto

class CommandType(Enum):
    PING = auto()
    MOVE = auto()
    GRIPPER = auto()
    HOME = auto()
    WAIT = auto()
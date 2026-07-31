from enum import Enum, auto

class CommandType(Enum):
    PING = auto()
    MOVE = auto()
    MAGNET_ON = auto()
    MAGNET_OFF = auto()
    HOME = auto()
    
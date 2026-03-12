from enum import Enum, auto

class CommandType(Enum):
    MOVE_TO = auto()
    HOME = auto()

    MAGNET_ON = auto()
    MAGNET_OFF = auto()
    
    WAIT = auto()
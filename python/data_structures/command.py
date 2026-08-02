from data_structures import CommandType

class Command:
    def __init__(self, type: CommandType, arg1 = None, arg2 = None, arg3 = None):
        self.type = type
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def expected_timeout(self, base_timeout: int = 2000) -> int:
        if self.type == CommandType.WAIT:
            return self.arg1 + 1000
        return base_timeout

    def to_bytes(self) -> bytes:
        '''Serializes this Command into the encoded format expected by the microcontroller.'''
        parts = [self.type.name]

        for arg in (self.arg1, self.arg2, self.arg3):
            if arg is not None:
                parts.append(str(arg))

        return " ".join(parts).encode() + b"\n"

    @classmethod
    def ping(cls) -> "Command":
        return cls(CommandType.PING)

    @classmethod
    def home(cls) -> "Command":
        return cls(CommandType.HOME)

    @classmethod
    def gripper(cls, state: int) -> "Command":
        return cls(CommandType.GRIPPER, state)

    @classmethod
    def move(cls, x: int, y: int, z: int) -> "Command":
        return cls(CommandType.MOVE, x, y, z)

    @classmethod
    def wait(cls, ms: int) -> "Command":
        return cls(CommandType.WAIT, ms)
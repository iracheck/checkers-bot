from dataclasses import dataclass, field

@dataclass
class Move:
    """Represents a single move or jump chain. To be processed as an input command to the ESP32.
    
    Attributes:
        path: The sequence of coordinates the piece moves through.
        captures: The coordinates of captured enemy pieces.
    """
    path: list[tuple[int,int]] = field(default_factory=list)
    kills: list[tuple[int,int]] = field(default_factory=list)
from abc import ABC, abstractmethod

from game.piece import Piece
from game.move import Move

class Player(ABC):

    color = "B"

    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def get_move(self) -> Move:
        pass
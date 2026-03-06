from abc import ABC, abstractmethod

from game.move import Move
from game.board import Board

class Player(ABC):
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def get_move(self, board: Board) -> Move:
        pass
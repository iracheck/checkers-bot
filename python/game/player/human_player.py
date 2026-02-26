
class Player:
    from abc import ABC, abstractmethod
    from game.piece import Piece

    color = "B"

    def __init__(self):
        pass

    @abstractmethod
    def get_move(self) -> Move:
        pass
from game.player.player import Player
from game.move import Move
from game.board import Board

class HumanPlayer(Player):
    def __init__(self, color="W"):
        super().__init__(color=color)

    def get_move(self, board: Board, turn: int) -> Move:
        return None


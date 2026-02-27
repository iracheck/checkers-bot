from game.player import Player
from game.move import Move
from game.board import Board
    
class AIPlayer(Player):
    def __init__(self, color="B"):
        super().__init__(color=color)

    def get_move(self, board: Board) -> Move:
        pass

    def minimax():
        pass

    def evalulate(move: Move) -> int:
        pass
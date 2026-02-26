from game.player import Player
from game.move import Move
    
class AIPlayer(Player):
    def __init__(self, color="B"):
        super().__init__(color=color)

    def get_move(self) -> Move:
        pass
from game.player.player import Player
from game.move import Move


class HumanPlayer(Player):
    def __init__(self, color="W"):
        super().__init__(color=color)

    def get_move(self) -> Move:
        move_str = input("Enter your move (e.g., 'a3 b4'): ")
        return move_str
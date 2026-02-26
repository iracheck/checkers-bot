from game.player.player import Player


class LLMPlayer(Player):
    def __init__(self, color="B"):
        super().__init__(color=color)

    def get_move(self):
        return NotImplementedError("LLMPlayer is not implemented yet")
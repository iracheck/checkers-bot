from dataclasses import dataclass

from game.player.player import Player
from game.board import Board
from game.move import Move

@dataclass
class LLMType:
    OPENAI = "CHATGPT"
    GOOGLE = "GEMINI"
    ANTHROPIC = "CLAUDE"


class LLMPlayer(Player):
    def __init__(self, color="B"):
        super().__init__(color=color)

    def get_move(self, board: Board) -> Move:
        return NotImplementedError("LLMPlayer is not implemented yet")
from game import Board
from game import Piece
from game.player import HumanPlayer, AIPlayer, LLMPlayer

board = Board()
player1 = HumanPlayer(Piece.WHITE)
player2 = AIPlayer(Piece.BLACK)

print("Initial Board:")
print(board)

board.move(1,2,2,3)

# print("Player 1 (White) move:")
# move1 = player1.get_move(board)
# print(f"Player 1 move: {move1}")

print("Has won for WHITE:", board.has_won(Piece.WHITE))

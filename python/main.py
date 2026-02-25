from game import Board
from game import Piece

board = Board()

board.get(1,2).promote()
board.move(1,2, 2,3)
print(board.get_every_legal(Piece.BLACK))
print(board)


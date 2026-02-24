from game import Board
from game import Piece

board = Board()
print(board)
print(board.get(4,5))
board.get(4,5).promote()
print(board.get(4,5))
print(board)
board.move(4,5,3,2)
print(board.get_num_pieces(Piece.BLACK))
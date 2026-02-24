from game import Board
from game import Piece

board = Board()
print(board)
print(board.get(4,5))
board.promote(4,5)
print(board.get(4,5))
print(board)
print(board.get_all_pieces())
print(board.get_num_pieces(Piece.WHITE))
print(board.get_every_legal(Piece.WHITE))
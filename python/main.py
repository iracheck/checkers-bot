from game import Board
from game import Piece

board = Board()

board.get(1,2).promote()
board.move(1,2, 2,3)
board.move(0,5,1,4)
board.set(2,7, None)
print(board.get_legal(2,3))
print(board)


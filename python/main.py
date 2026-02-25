from game import Board
from game import Piece

board = Board()

board.get(1,2).promote()
print(board.move(1,2, 2,3))
print(board.move(0,5,1,4))
board.set(2,7,None)
print("From (2,3): " + str(board.get_legal(2,3)))
print(board)
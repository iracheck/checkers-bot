import time

from game import Board
from game import Piece
from game.player import HumanPlayer, AIPlayer, LLMPlayer, LLMType
from interface import SerialCom
from computer_vision import ComputerVision

print("Initializing components...")
board = Board()
vision = ComputerVision()
serial_com = SerialCom()
player1 = AIPlayer(5, Piece.WHITE)
player2 = AIPlayer(5, Piece.BLACK)

# vision.run()

# try:
#     serial_com.connect()
# except:
#     print("No serial device is connected")

start_time = time.perf_counter()

turn = 1
running = True
while running:
    if turn % 2 == 1:
        move = player1.get_move(board, turn)
    else:
        move = player2.get_move(board, turn)

    if turn > 100:
        running = False

    board.move(move)
    if len(move.kills) > 0:
        print(f"Piece ({move.origin[0]}, {move.origin[1]}) was moved to ({move.path[-1][0]}, {move.path[-1][1]}) and killed the following pieces: {move.kills}")
    else:
        print(f"Piece ({move.origin[0]}, {move.origin[1]}) was moved to ({move.path[-1][0]}, {move.path[-1][1]})")
    print(board)

    if board.has_won(player1.color):
        print("Player 1 wins!")
        running = False
    elif board.has_won(player2.color):
        print("Player 2 wins!")
        running = False
    
    turn += 1

end_time = time.perf_counter()

print("Done after " + str(turn) + " turns")
print("Game took: " + str(end_time - start_time) + " seconds.")
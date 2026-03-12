from game import Board
from game import Piece
from game.player import HumanPlayer, AIPlayer, LLMPlayer

board = Board()
player1 = AIPlayer(Piece.WHITE)
player2 = AIPlayer(Piece.BLACK)

print("Initial Board:")
print(board)

running = True
turn = 1
while running:
    if turn % 2 == 1:
        move = player1.get_move(board, turn)
    else:
        move = player2.get_move(board, turn)

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

print("Done after " + str(turn) + " turns")
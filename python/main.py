import time
import argparse
import tracemalloc

from game import Board
from game import Piece
from game.player import HumanPlayer, AIPlayer, LLMPlayer, LLMType
from interface import SerialCom, SequenceRunner
from computer_vision import ComputerVision
from data_structures.sequence import Sequence, Command

# INFORMATION TEXT
PLAYER_SELECTION_HELP = "Options: 'Human' 'AI[x]' 'Google' (E.g. AI5 is AI with difficulty 5)"

def main(args):
    DEBUG = False
    if args.debug:
        DEBUG = True

    if DEBUG: 
        start_time = time.perf_counter()
    
    print("Initializing components...")
    board = Board()
    vision = ComputerVision()
    serial_com = SerialCom(True, DEBUG)
    runner = SequenceRunner(serial_com)
    player1 = getPlayer(args.player1, Piece.WHITE)
    player2 = getPlayer(args.player2, Piece.BLACK)

    turn = 0
    running = True

    # try:
    #     serial_com.connect()
    # except TypeError as e:
    #     if DEBUG: print(e)

    runner.run(Sequence([Command.wait(2500)]))

    while running:
        turn += 1

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
        if DEBUG: print(board)

        if board.has_won(player1.color):
            print("Player 1 wins!")
            running = False
        elif board.has_won(player2.color):
            print("Player 2 wins!")
            running = False

    print("Done after " + str(turn) + " turns")

    
    if DEBUG: 
        end_time = time.perf_counter()
        print("Game took: " + str(end_time - start_time) + " seconds.")


def getPlayer(arg: str, color: str):
    if arg[0:2] == "ai":
        return AIPlayer(int(arg[2]), color)
    elif arg == "Gemini":
        return LLMPlayer(LLMType.GOOGLE, color)
    elif arg == "Human":
        return HumanPlayer(color)
    else:
        print("Player for color " + color + " is of an invalid type. " + PLAYER_SELECTION_HELP)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--debug", "--d", action="store_true", help="Run in debug (verbose) mode. Also shows time benchmarking data")
    parser.add_argument("player1", type=str, help="The type of player 1. " + PLAYER_SELECTION_HELP)
    parser.add_argument("player2", type=str, help="The type of player 2. " + PLAYER_SELECTION_HELP)

    return parser.parse_args()




if __name__ == "__main__":
    args = parse_args()
    main(args)
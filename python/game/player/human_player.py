from game.player.player import Player
from game.move import Move
from game.board import Board

class HumanPlayer(Player):
    def __init__(self, color="W"):
        super().__init__(color=color)

    def get_move(self, board: Board):
        invalid = True
        print("\n"*100)

        # Print the current state of the board at the start of the players turn, so that they can make an informed decision about their move
        print(board)

        # Loop until the player inputs something valid
        while (invalid):
            move_str = input("YOUR TURN:\nOptions:\na) Move (Usage: 'move 1 2 2 3')\nb) List Legal Moves (Usage: 'list')\nInput: ")
            if move_str.strip() == "list":
                print("Legal Moves:")
                for move in board.get_every_legal(self.color):
                    if len(move) > 0:
                        print(move)
            elif move_str.startswith("move"):
                move_str = move_str[4:].strip()
                move_str = move_str.split(" ")

                for i in range(len(move_str)):
                    move_str[i] = int(move_str[i])

                x1 = move_str[0]
                y1 = move_str[1]
                x2 = move_str[2]
                y2 = move_str[3]
                
                if (x2,y2) in any(i.path in board.get_legal(x1,y1) where boa):
                    board.move(x1,y1,x2,y2)
                    invalid = False
                else:
                    print("[error] For one reason or another, that move was invalid. Try again.")
            else:
                print("[error] Invalid input, please try again.")
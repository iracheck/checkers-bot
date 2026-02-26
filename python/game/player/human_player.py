from game.player.player import Player
from game.move import Move
from game.board import Board

class HumanPlayer(Player):
    def __init__(self, color="W"):
        super().__init__(color=color)

    def get_move(self, board: Board) -> Move:
        invalid = True
        valid_moves = board.get_every_legal(self.color)

        print("\n"*100)

        print(board)

        self.display_valid_moves(valid_moves)
        print(valid_moves)


        # Loop until the player inputs something valid
        while (invalid):
            move_str = input("YOUR TURN:\nOptions:\na) Move (Usage: 'move 1 2 option_id')\n")
            move_str = move_str.split(" ")
            if len(move_str) != 4:
                print("Invalid input. Please try again.")
                continue
            else:
                command, x, y, option_id = move_str
                if command != "move":
                    print("Invalid command. Please try again.")
                    continue
                else:
                    try:
                        x = int(x)
                        y = int(y)
                        option_id = int(option_id)
                    except ValueError:
                        print("Invalid input. One of your inputs for x, y, or option_id is not an integer. Try again.")
                        continue
                    
                    if (x,y) not in valid_moves.keys():
                        print("Invalid piece. Please try again.")
                        continue
                    elif option_id >= len(valid_moves[(x,y)]):
                        print("Invalid option. Please try again.")
                        continue
                    else:
                        invalid = False
                        return valid_moves[(x,y)][option_id]

    def display_valid_moves(self, valid_moves: dict[tuple[int, int], list[Move]]):
        for coord, coord_moves in valid_moves.items():
            if len(coord_moves) == 0:
                continue

            print(f"Piece at {coord} has the following moves:")
            for move in coord_moves:
                print(f"{coord_moves.index(move)})) {move}")


from game.piece import Piece

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        
        self.setup()
        
    # board state
    def setup(self):
        """Resets all pieces to their traditional location on an 8x8 checkers board"""
        for y in range(0, 3):
            for x in range(0, 8):
                if not self.is_unplayable_space(x,y):
                    self.set(x, y, Piece(Piece.BLACK)) 
                    
        for y in range(5,8):
            for x in range(0,8):
                if not self.is_unplayable_space(x,y):
                    self.set(x,y, Piece(Piece.WHITE))
    
    # grid interactions
    def get(self, x, y) -> Piece | None:
        """Returns the object currently occupying a coordinate on the board, or 'None' if it is empty"""
        return self.board[y][x]
    
    def set(self, x, y, piece):
        """Sets a specific coordinate on the board to the specified object"""
        self.board[y][x] = piece
        
    # game logic
    def move(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """If valid, moves a piece to a given position. For forceful movements, use 'set(x,y,piece)'"""
        pass
    
    def get_legal(self, x, y):
        """Returns a list of legal moves from a given position"""
        pass
    
    def get_all_legal(self, color):
        """Returns a list of list legal moves for ALL pieces of this color"""
        pass
    
    def has_won(self, color) -> bool:
        """Returns True if the color team has won"""
        pass
    
    def get_all_pieces(self, color):
        """Returns a list of all alive pieces of this color"""
        pass
    
    def get_num_pieces(self, color) -> int:
        """Returns the number of alive pieces of this color"""
        num = 0
        
        for y in range(0,8):
            for x in range(0,8):
                if self.is_occupied(x,y):
                    occupant = self.get(x,y)
                    if occupant is Piece and occupant.color == color:
                        num += 1

    # helpers
    def is_unplayable_space(self, x, y) -> bool:
        """Returns if a space is a 'black' square, or unplayable"""
        if (x + y) % 2 == 1:
            return False
        else:
            return True
        
    def is_occupied(self, x, y) -> bool:
        """Returns if a space is occupied"""
        return self.board[y][x] != None
    
    
    # overrides    
    def __str__(self):
        board_str = ""
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if isinstance(piece, Piece):
                    board_str += str(piece) + " "
                elif not self.is_unplayable_space(x, y):
                    board_str += "|||| "
                elif piece is None:
                    board_str += "---- "
                    
            board_str += "\n"
        return board_str
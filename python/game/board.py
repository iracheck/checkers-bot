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
    
    # board-piece interaction
    def move(self, x1: int, y1: int, x2: int, y2: int, force = False) -> bool:
        """If valid, moves a piece to a given position.. Will also attempt to promote pieces that are at the border'"""
        pass
    
    def get_legal(self, x, y):
        """Returns a list of legal moves from a given position"""
        pass
    
    def promote(self, x, y) -> bool:
        if self.is_occupied(x,y):
            self.get(x,y).promote()
            return True
        return False
    
    # game logic
    def get_all_legal(self, color):
        """Returns a list of list legal moves for ALL pieces of this color"""
        pass
    
    #TODO: Update it so if the enemy has no pieces OR legal moves, you win
    def has_won(self, color) -> bool:
        """Returns whether a team has won the game or not"""
        if color == Piece.BLACK and self.get_num_pieces(Piece.WHITE) == 0:
            return True
        elif color == Piece.WHITE and self.get_num_pieces(Piece.BLACK) == 0:
            return True
        else:
            return False
        
    def get_all_pieces(self):
        """Returns a list of every piece currently on the board"""
        return self.get_all_pieces_of_team(Piece.WHITE) + self.get_all_pieces_of_team(Piece.BLACK)
    
    def get_all_pieces_of_team(self, color):
        """Returns a list of all pieces belonging to a specific color"""
        pieces = []
        
        for y in range(0,8):
            for x in range(0,8):
                if self.is_occupied(x,y):
                    occupant = self.get(x,y)
                    if isinstance(occupant, Piece) and occupant.color == color:
                        pieces.append(occupant)
        return pieces
    
    def get_num_pieces(self, color) -> int:
        """Returns the number of alive pieces of this color"""
        return len(self.get_all_pieces_of_team(color))

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
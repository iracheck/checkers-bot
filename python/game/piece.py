class Piece:
    WHITE = "W"
    BLACK = "B"
    
    def __init__(self, color, king=False):
        self.color = color
        self.is_king = king
        
    def promote(self):
        self.is_king = True

    def __str__(self):
        return f"{'K' if self.is_king else 'P'}({self.color})"

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented

        return self.color == other.color and self.is_king == other.is_king
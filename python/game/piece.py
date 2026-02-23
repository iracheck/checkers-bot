class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king
        
    def promote(self):
        self.king = True

    def __str__(self):
        return f"{'K' if self.king else 'P'}({self.color})"
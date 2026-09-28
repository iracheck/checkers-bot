class BoardDiff:
    def __init__(self):
        self.is_same = True
        self.new = []
        self.destroyed = []
        self.invalid = []

    def __str__(self):
        return f"New Pieces: {str(self.new)}, Destroyed Pieces: {str(self.destroyed)}, Invalid Pieces:{str(self.invalid)}"



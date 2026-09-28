class BoardDiff:
    def __init__(self):
        self.is_same = True
        self.created = list[tuple(int, int)]
        self.destroyed = list[tuple(int, int)]
        self.invalid = list[tuple(int, int)]

    def __str__(self):
        return f"New Pieces: {str(self.created)}, Destroyed Pieces: {str(self.destroyed)}, Invalid Pieces:{str(self.invalid)}"



from game.board import Board
from game.piece import Piece


def test_promotion():
    board = Board()
    board.clear()

    # manually set up a piece at the edge of the board
    board.set(0, 1, Piece(Piece.WHITE))
    board.move(0, 1, 1, 0)

    assert board.get(1, 0).is_king == True
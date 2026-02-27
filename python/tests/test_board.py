from game.board import Board
from game.piece import Piece


def test_move():
    board = Board()
    board.clear()

    board.set(0, 1, Piece(Piece.WHITE))
    board.move(0, 1, 1, 0)

    assert board.get(1, 0) is not None

def test_promotion():
    board = Board()
    board.clear()

    board.set(0, 1, Piece(Piece.WHITE))
    board.move(0, 1, 1, 0)

    assert board.get(1, 0).is_king == True

def test_no_legal_moves_when_stuck():
    board = Board()
    board.clear()

    board.set(7, 2, Piece(Piece.WHITE))
    board.set(6, 1, Piece(Piece.BLACK))
    board.set(5,0, Piece(Piece.BLACK))

    print(board)

    legal_moves = board.get_legal(7,2)

    assert len(legal_moves) == 0

def test_one_legal_move_when_partially_blocked():
    board = Board()
    board.clear()

    board.set(0, 1, Piece(Piece.WHITE))

    legal_moves = board.get_legal(0, 1)
    assert len(legal_moves) == 1

def test_one_legal_with_kill():
    board = Board()
    board.clear()

    board.set(0, 1, Piece(Piece.WHITE))

    legal_moves = board.get_legal(0, 1)
    assert len(legal_moves) == 1

def test_basic_jump():
    board = Board()
    board.clear()

    board.set(4, 3, Piece(Piece.WHITE))
    board.set(3, 2, Piece(Piece.BLACK))
    legal_moves = board.get_legal(4, 3)

    assert len(legal_moves) == 1
    assert legal_moves[0].kills[0] == (3, 2)
    assert legal_moves[0].path[0] == (2, 1)

def test_double_jump():
    board = Board()
    board.clear()

    board.set(6, 5, Piece(Piece.WHITE))
    board.set(5, 4, Piece(Piece.BLACK))
    board.set(3, 2, Piece(Piece.BLACK))

    legal_moves = board.get_legal(6, 5)

    assert len(legal_moves) == 1
    assert legal_moves[0].path == [(4, 3), (2, 1)]
    assert legal_moves[0].kills == [(5, 4), (3, 2)]

def test_double_jump_two_choices():
    board = Board()
    board.clear()

    board.set(6, 5, Piece(Piece.WHITE))
    board.set(5, 4, Piece(Piece.BLACK))
    board.set(3, 2, Piece(Piece.BLACK))
    board.set(5, 2, Piece(Piece.BLACK))

    print(board)

    legal_moves = board.get_legal(6, 5)

    assert len(legal_moves) == 2
    assert len(legal_moves[0].kills) == 2
    assert len(legal_moves[1].kills) == 2
    

def test_jump_removes_captured_piece():
    board = Board()
    board.clear()

    board.set(4, 3, Piece(Piece.WHITE))
    board.set(3, 2, Piece(Piece.BLACK))

    board.move(4, 3, 2, 1)

    assert board.get(3, 2) is None

def test_king_can_move_backwards():
    board = Board()
    board.clear()

    board.set(4, 3, Piece(Piece.WHITE))
    board.promote(4,3)

    legal_moves = board.get_legal(4, 3)

    assert len(legal_moves) == 4    

def test_king_can_jump_backwards():
    board = Board()
    board.clear()

    board.set(4, 3, Piece(Piece.WHITE))
    board.promote(4,3)
    board.set(5, 4, Piece(Piece.BLACK))

    print(board)

    legal_moves = board.get_legal(4, 3)

    assert len(legal_moves) == 1

def test_forced_jump():
    board = Board()
    board.clear()

    board.set(4, 3, Piece(Piece.WHITE))
    board.set(3, 2, Piece(Piece.BLACK))

    legal_moves = board.get_legal(4, 3)

    assert len(legal_moves) == 1

def test_has_won_from_last_standing():
    board = Board()
    board.clear()

    # Test enemies all dead
    board.set(0, 1, Piece(Piece.WHITE))

    assert board.has_won(Piece.WHITE) == True
    assert board.has_won(Piece.BLACK) == False

def test_has_won_from_blockade():
    board = Board()
    board.clear()

    # Test blocked
    board.set(0, 1, Piece(Piece.WHITE))
    board.set(1, 0, Piece(Piece.BLACK))

    assert board.has_won(Piece.WHITE) == False
    assert board.has_won(Piece.BLACK) == True
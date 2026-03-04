from game.player import Player
from game.move import Move
from game.board import Board
from game.piece import Piece

import copy
    
class AIPlayer(Player):
    def __init__(self, color):
        super().__init__(color=color)

    def get_move(self, board: Board) -> Move:
        flat_moves = [move for moves in board.get_every_legal(self.color).values() for move in moves]

        best_move = None
        best_score = float('-inf')

        for move in flat_moves:

            sim_board = copy.deepcopy(board)

            # move the result, and consider the scenario in which the result is not valid
            result = sim_board.move(move)
            if not result:
                continue

            score = self.minimax(sim_board, 4, False)

            if best_move is None or score > best_score:
                best_move = move
                best_score = score

        return best_move

    def minimax(self, board: Board, depth: int, is_maximizing: bool) -> float:
        if depth == 0:
            return self.evalulate(board)
        
        color = self.color if is_maximizing else self.opposing_color()
        all_moves = board.get_every_legal(color)

        flat_moves = [move for moves in all_moves.values() for move in moves]

        if len(flat_moves) == 0:
            print("No moves avaliable")

        print(f"depth={depth}, is_maximizing={is_maximizing}, flat_moves={len(flat_moves)}")
        if is_maximizing:
            best = float('-inf')
            for move in flat_moves:
                sim_board = copy.deepcopy(board)
                sim_board.move(move)
                score = self.minimax(sim_board, depth - 1, False)
                best = max(best, score)
            return best
        else:
            best = float('inf')
            for move in flat_moves:
                sim_board = copy.deepcopy(board)
                sim_board.move(move)
                score = self.minimax(sim_board, depth - 1, True)
                best = min(best, score)
            return best


    def evalulate(self, board: Board) -> float:
        opposing_color = Piece.BLACK
        if (opposing_color == self.color):
            opposing_color = Piece.WHITE

        if board.has_won(self.color):
            return 999999999999
        elif board.has_won(opposing_color):
            return -999999999999

        score_from_center = 0.0

        # controlling the center is seen as a slight benefit
        for piece in board.get_all_pieces_in_area(2, 2, 5, 5):
            if board.get(piece[0], piece[1]).color != self.color:
                score_from_center -= 0.05
            else:
                score_from_center += 0.1

        score_from_pieces = 0.0

        friendly_pieces = board.get_all_pieces_of_team(self.color)
        enemy_pieces = board.get_all_pieces_of_team(opposing_color)

        # the AI cares only slightly more about getting kings than preserving the lives of its pawns
        for piece in friendly_pieces:
            score_from_pieces += 0.5
            if board.get(piece[0], piece[1]).is_king:
                score_from_pieces += 0.1


        # the AI cares much more about preventing enemy from getting kings than killing enemy pieces
        for piece in enemy_pieces:
            score_from_pieces -= 0.2
            if board.get(piece[0], piece[1]).is_king:
                score_from_pieces -= 0.5

        # apply a flat detriment for having "less pieces" than the enemy
        if len(friendly_pieces) < len(enemy_pieces):
            score_from_pieces -= 2

        return score_from_center + score_from_pieces

    def opposing_color(self) -> str:
        if self.color == Piece.BLACK:
            return Piece.WHITE
        else:
            return Piece.BLACK

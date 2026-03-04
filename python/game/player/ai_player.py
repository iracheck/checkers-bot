from game.player import Player
from game.move import Move
from game.board import Board
from game.piece import Piece

import copy
import random
    
class AIPlayer(Player):
    def __init__(self, color):
        super().__init__(color=color)
        self.num_turns = 0

    def get_move(self, board: Board, num_turns: int) -> Move:
        '''Get move function that is required by the game in order to get the players' next move'''
        flat_moves = [move for moves in board.get_every_legal(self.color).values() for move in moves]
        self.num_turns = num_turns

        best_move = None
        best_score = float('-inf')

        for move in flat_moves:

            sim_board = copy.deepcopy(board)

            # move the result, and consider the scenario in which the result is not valid
            result = sim_board.move(move)
            if not result:
                continue

            score = self.minimax(sim_board, 50, False)

            if best_move is None or score > best_score:
                best_move = move
                best_score = score

        return best_move

    def minimax(self, board: Board, depth: int, is_maximizing: bool, alpha=float('-inf'), beta=float('inf')) -> float:
        '''A recursive function that analyzes every possible outcome of a board and evaluates it, to find the best possible move for the AI'''
        if depth == 0:
            return self.evalulate(board)
        
        color = self.color if is_maximizing else self.opposing_color()
        all_moves = board.get_every_legal(color)

        flat_moves = [move for moves in all_moves.values() for move in moves]

        # print(f"depth={depth}, is_maximizing={is_maximizing}, flat_moves={len(flat_moves)}")
        if is_maximizing:
            best = float('-inf')
            for move in flat_moves:
                sim_board = copy.deepcopy(board)
                sim_board.move(move)
                score = self.minimax(sim_board, depth - 1, False, alpha, beta)
                best = max(best, score)

                alpha = max(beta,best)
                if beta >= alpha:
                    break
            return best
        else:
            best = float('inf')
            for move in flat_moves:
                sim_board = copy.deepcopy(board)
                sim_board.move(move)
                score = self.minimax(sim_board, depth - 1, True, alpha, beta)
                best = min(best, score)

                beta = min(beta, best)
                if beta >= alpha:
                    break
            return best


    def evalulate(self, board: Board) -> float:
        '''Returns a float that says how 'favorable' a board is to the AI'''
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
                score_from_center -= 0.2
            else:
                score_from_center += 0.1

        score_from_pieces = 0.0

        friendly_pieces = board.get_all_pieces_of_team(self.color)
        enemy_pieces = board.get_all_pieces_of_team(opposing_color)

        # the AI cares only slightly more about getting/keeping kings than preserving the lives of its pawns, but it really loves keeping its pawns alive
        for piece in friendly_pieces:
            score_from_pieces += 0.8
            if board.get(piece[0], piece[1]).is_king:
                score_from_pieces += 0.1


        # the AI cares much more about preventing enemy from getting kings than killing enemy pieces
        for piece in enemy_pieces:
            score_from_pieces -= 0.2
            if board.get(piece[0], piece[1]).is_king:
                score_from_pieces -= 0.8

        # apply a flat bonus for having "more pieces" than the enemy to encourage killing
        pieces_diff = len(friendly_pieces) - len(enemy_pieces)
        if pieces_diff > 0:
            score_from_pieces *= pieces_diff

        score_from_num_moves = 0

        moves = board.get_every_legal(self.color)
        for move in moves:
            for option in move:
                score_from_num_moves += 0.2
         

        return score_from_center + score_from_pieces + score_from_num_moves + random.uniform(-0.25, 0.25)

    def opposing_color(self) -> str:
        '''Returns the color that this AI Player is *not*'''
        if self.color == Piece.BLACK:
            return Piece.WHITE
        else:
            return Piece.BLACK
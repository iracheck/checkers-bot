# Board generation
import numpy as np
import cv2

from computer_vision import ComputerVision
from game import Board, Piece, Move

class BoardGenerator():
    def __init__(self, cv: ComputerVision, dimensions=8, debug=False):
        self.cv = cv
        self.dimensions = dimensions
        self.DEBUG = debug

    def get(self, display=False):
        '''Gets a board from the current camera input.
        
        `display`: debug tool to see output visualized'''
        frame = self.cv.get_frame()
        return self.get_from(frame)
        
    def get_from(self, frame, current_board: Board, moving_player: str):
        '''
        Creates a board given a specific frame (image) as input, and then verify it
        
        `frame`: the frame to convert into a board\n
        `current_board`: the board that is currently registered as the "current board," aka the board that was generated following the previous move
        '''

        new_board = Board(setup=False)

        for i in range(0, self.dimensions):
            for j in range(0, self.dimensions):
                sqr = self.cv.squares[(i,j)]
                old_piece = current_board.get(i, j)

                # Use camera input to get pieces, and use known values from previous board to deduce if its a king or not
                color = self.sample_color_in_region(frame, sqr[0], sqr[1], sqr[2], sqr[3])

                if old_piece is not None and old_piece.color == color:
                    new_board.set(i, j, Piece(color, old_piece.is_king))
                else:
                    new_board.set(i, j, Piece(color, False))

        # Determine what changed between the previous board and the camera generated board.
        diff = new_board.get_diff(current_board)

        if diff.is_same:
            return None

        if not self.is_board_valid(new_board, current_board, moving_player):
             return None

        return new_board
                        
                

    def is_board_valid(self, new_board: Board, old_board: Board, color_of_moving_player: str) -> "Move":
        moves = old_board.get_every_legal(color_of_moving_player)

        for move in moves:
            temp_board = old_board.copy()
            temp_board.move(move)

            if temp_board.equals(new_board):
                return move
        

    # Color Getting
    
    def sample_color_in_region(self, frame, x1: int, y1: int, x2: int, y2: int) -> str:
            '''Returns a color in the form of a string. e.g. `RED` `WHITE` `BLACK`
            
            `frame` represents the image to be sampled.
    
            `x1,x2,y1,y2` represent the bounds of which are sampled'''
            region = frame[y1:y2, x1:x2]
    
            average_color = np.mean(region, axis=(0, 1))
    
            return self.classify_color(average_color)
    
    @staticmethod
    def classify_color(bgr_color) -> str | None:
            '''Converts a sampled BGR color into an english color name.
            
            `bgr_color`: an array-like [B, G, R], e.g. from np.mean(region, axis=(0,1))

            Returns a color as defined in Piece (Piece.WHITE `"W"` or Piece.BLACK `"B"`)
            '''
            # Reshape to a 1x1 pixel "image" so cv2 can convert it
            bgr_pixel = np.uint8([[bgr_color]])
            hsv_pixel = cv2.cvtColor(bgr_pixel, cv2.COLOR_BGR2HSV)[0][0]
            h, s, v = int(hsv_pixel[0]), int(hsv_pixel[1]), int(hsv_pixel[2])
    
            # Low saturation + high value = white
            if s < 40 and v > 150:
                return Piece.WHITE
    
            # Low saturation + low value = black
            if v < 60:
                return Piece.BLACK
            
            return None
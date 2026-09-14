# Board generation
import numpy as np
import cv2

from computer_vision import ComputerVision
from game import Board, Piece

class BoardGenerator():
    def __init__(self, cv: ComputerVision, dimensions=8):
        self.cv = cv
        self.dimensions = dimensions

    def get(self, display=False):
        '''Gets a board from the current camera input.
        
        `display`: debug tool to see output visualized'''
        frame = self.cv.get_frame()
        return self.get_from(frame)
        
    def get_from(self, frame, display=False):
        '''Creates a board given a specific frame (image) as input
        
        `frame`: the frame to convert into a board
        `display`: debug tool to see output visualized'''

        board = Board(setup=False)

        for i in range(0, self.dimensions):
            for j in range(0, self.dimensions):
                sqr = self.cv.squares[(i,j)]
                color = self.sample_color_in_region(frame, sqr[0], sqr[1], sqr[2], sqr[3])
                if color:
                    board.matrix[i][j] = Piece(color)

    def is_board_valid(self, new_board: Board, old_board: Board, color_of_moving_player: str):
        moves = old_board.get_every_legal(color_of_moving_player)

        for move in moves:
            temp_board = old_board.copy()
            
        

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
            '''Converts a sampled BGR color into a human-readable color name.
            
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
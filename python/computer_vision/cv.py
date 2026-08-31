import cv2
import numpy as np
import json
import os

from game import Board, Piece

class ComputerVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.corners = None
        self.squares = None

        self.output_size = 800
        self.dimensions = 8

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not self.cap.isOpened():
            raise Exception("Failed to open camera!")

    # Calibration

    def load_calibration(self, target):
        '''Loads existing calibration data from json located at `target`'''
        with open(target, "r") as file:
            data = json.load(file)
        return data

    def save_calibration(self, data, target):
        '''Saves existing calibration `data` to json file located at `target`''' 
        with open(target, "w") as file:
            json.dump(data, file)

    def calibrate(self, recalibrate, target="calibration.json"):
        '''Runs the calibration process-- loads an existing calibration if it exists and recalibration is not occuring, otherwise prompts the user with a new calibration process.
        '''
        self.squares = self.get_square_locations()

        if not recalibrate and os.path.exists(target):
            print("Loading existing calibration...")
            self.corners = self.load_calibration(target)
            return

        print("Running calibration...")
        self.corners = self.calibrate_corners()
        self.save_calibration(self.corners, target)

    def calibrate_corners(self):
        '''Runs the calibration process for the computer vision system, allowing '''
        points = []
        waiting = True

        def on_click(event, x, y, flags, param):
            nonlocal waiting
            if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
                waiting = False
                points.append((x, y))
                print(f"Point {len(points)}: ({x}, {y})")

        for corner in range(0, 4):
            ret, frame = self.cap.read()
            waiting = True

            for pt in points:
                for pt2 in points:
                    cv2.line(frame, pt, pt2, (0, 255, 0), 2)
                cv2.circle(frame, pt, 5, (0, 255, 0), -1)

            cv2.imshow("Select corners in a clockwise fashion, starting from the top left", frame)
            cv2.setMouseCallback("Select corners in a clockwise fashion, starting from the top left", on_click)

            while waiting:
                cv2.waitKey(1)
            cv2.destroyAllWindows()

        ret, frame = self.cap.read()
        warped = self.warp_board(frame, points)

        # Draw preview of squares
        for square in self.squares:
            loc = self.squares.get(square)
            cv2.line(warped, (loc[0], loc[1]), (loc[0], loc[3]), (0, 0, 0), 1)
            cv2.line(warped, (loc[0], loc[1]), (loc[2], loc[1]), (0, 0, 0), 1)
        cv2.imshow("Preview - press 'r' to redo, any other key to accept", warped)

        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key == ord('r'):
            print("Redoing calibration...")
            return self.calibrate_corners()

        return points

    def get_square_locations(self):
        '''Gets all the squares given the exist'''
        squares = {}
        square_size = self.output_size // self.dimensions
        print(square_size)

        for row in range(0, self.dimensions):
            for col in range(0, self.dimensions):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                squares[(row,col)] = (x1, y1, x2, y2)

        return squares

    # Board transformations

    def warp_board(self, frame, corners):
        """
        frame: the frame to be warped

        corners: list of 4 (x,y) points in the RAW frame, in order:
        top-left, top-right, bottom-right, bottom-left
        """
        src = np.array(corners, dtype="float32")

        dst = np.array([
            [0, 0],
            [self.output_size - 1, 0],
            [self.output_size - 1, self.output_size - 1],
            [0, self.output_size - 1]
        ], dtype="float32")

        matrix = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(frame, matrix, (self.output_size, self.output_size))

        return warped

    # Board generation
    def generate_board_from_image(self, frame) -> Board:

        for i in range(0, self.dimensions):
            for j in range(0, self.dimensions):
                dimensions = self.squares[(i,j)]
                color = self.sample_color_in_region(frame, dimensions[0], dimensions[1], dimensions[2], dimensions[3])
                


    def sample_color_in_region(self, frame, x1: int, y1: int, x2: int, y2: int):
        '''Gets the average of the colors located in a given region.
        
        `frame` represents the image to be sampled.

        `x1,x2,y1,y2` represent the bounds of which are sampled'''
        region = frame[y1:y2, x1:x2]

        average_color = np.mean(region, axis=(0, 1))

        return average_color

    # temp method for testing
    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to capture frame")
                break
            
            if not self.corners:
                print('not self corner')
                self.corners = self.calibrate_corners()

            frame = cv2.flip(frame, 1)

            # for s in self.squares.values():
            #     color = self.sample_color_in_region(frame, s[0], s[1], s[2], s[3])
            #     cv2.putText(frame, str(color), (s[0],s[1]), cv2.FONT_HERSHEY_COMPLEX, 0.25, 0.1, 1)

            cv2.imshow("Live Video Feed", self.warp_board(frame, self.corners))

            # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
import cv2
import numpy as np
import json
import os

class ComputerVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.corners = None

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not self.cap.isOpened():
            raise Exception("Failed to open camera!")

    # def calibrate_corners(self):
    #     """Run once: click the 4 board corners in order (TL, TR, BR, BL)."""
    #     ret, frame = self.cap.read()
    #     points = []

    #     cv2.imshow("Click 4 corners: TL, TR, BR, BL", frame)
    #     cv2.setMouseCallback("Click 4 corners: TL, TR, BR, BL", on_click)

    #     while len(points) < 4:
    #         cv2.waitKey(1)

    #     cv2.destroyAllWindows()
    #     return points

    def warp_board(self, frame, corners, output_size=800):
        """
        corners: list of 4 (x,y) points in the RAW frame, in order:
                top-left, top-right, bottom-right, bottom-left
        output_size: side length (px) of the square output image
        """
        src = np.array(corners, dtype="float32")

        dst = np.array([
            [0, 0],
            [output_size - 1, 0],
            [output_size - 1, output_size - 1],
            [0, output_size - 1]
        ], dtype="float32")

        matrix = cv2.getPerspectiveTransform(src, dst)
        warped = cv2.warpPerspective(frame, matrix, (output_size, output_size))

        return warped

    # Calibration

    def load_calibration(self, target):
        '''Loads existing calibration data from json'''
        file = open(target)
        data = json.dump(file)

    def save_calibration(self, data, target):
        '''Saves existing calibration data to json'''
        json.dump(data, target)

    def calibrate(self, recalibrate, target="calibration.json"):
        '''Runs the calibration process-- loads an existing calibration if it exists and recalibration is not occuring, otherwise prompts the user with a new calibration process'''
        if not recalibrate and os.path.exists(target):
            print("Loading existing calibration...")
            return self.load_calibration(target)

        print("Running calibration...")
        points = self.calibrate_corners()
        self.save_calibration(points, target)
        return points

    def calibrate_corners(self):
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
        cv2.imshow("Preview - press 'r' to redo, any other key to accept", warped)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key == ord('r'):
            print("Redoing calibration...")
            return self.calibrate_corners()

        return points

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            self.calibrate_corners()

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            flipped = cv2.flip(hsv, 1)

            red_mask = cv2.inRange(flipped, (0, 100, 100), (10, 255, 255))
            black_mask = cv2.inRange(flipped, (0,0,0), (100, 255, 50))

            combined_mask = cv2.bitwise_or(red_mask, black_mask)

            blur = cv2.GaussianBlur(combined_mask, (9, 9), 2)

            

            cv2.imshow("Live Video Feed", frame)

            # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
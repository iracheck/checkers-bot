import cv2

class ComputerVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

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
                        cv2.line(frame, pt, pt2, 2, 2)
                     cv2.circle(frame, pt, 5, 2, 5)
                     

                cv2.imshow("Select corner " + str(corner), frame)
                cv2.setMouseCallback("Select corner " + str(corner), on_click)

                while waiting:
                     cv2.waitKey(1)
                cv2.destroyAllWindows()
        

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            self.calibrate_corners()

            return

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

    def get_board_image(self):
        ret, frame = self.cap.read()
        return frame
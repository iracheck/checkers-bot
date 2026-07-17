import cv2

class ComputerVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise Exception("Failed to open camera!")

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            red_mask = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
            black_mask = cv2.inRange(hsv, (0,0,0), (100, 255, 50))

            cv2.imshow("Live Video Feed", frame)

            # Press q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_board_image(self):
        ret, frame = self.cap.read()
        return frame
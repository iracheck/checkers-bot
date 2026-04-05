from computer_vision import ComputerVision

def test_open_camera():
    cv = ComputerVision()

    assert cv.cap is not None
    assert cv.cap.isOpened()
    
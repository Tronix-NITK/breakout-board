from .driver import Driver as DriverBase
import cv2


class Driver(DriverBase):
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        cv2.destroyWindow("cv driver")

    def push_frame(self, frame):
        cv2.imshow("cv driver", frame)
        cv2.waitKey(10)

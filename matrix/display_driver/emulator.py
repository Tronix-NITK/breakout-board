from matrix.display_driver.driver import Driver as DriverBase
import cv2


class Driver(DriverBase):
    def __init__(self, fps):
        self.frame_time = int(1000 / fps)

    def start(self):
        pass

    def stop(self):
        cv2.destroyWindow("emulator")

    def push_frame(self, frame):
        cv2.imshow("emulator", frame)
        cv2.waitKey(self.frame_time)

from matrix.display_driver.arduino import Driver
import numpy as np
from time import sleep


def main():
    port = "/dev/port"
    driver = Driver((5, 10), port, 9600)
    driver.start()
    frame = np.zeros((5, 10))
    i = 0
    try:
        while True:
            driver.push_frame(frame)
            sleep(1)
            i += 1
    except KeyboardInterrupt:
        pass
    finally:
        driver.stop()

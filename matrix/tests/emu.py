from matrix.display_driver.emulator import Driver
import numpy as np


def main():
    driver = Driver(fps=60)
    driver.start()
    frame = np.zeros((500, 500))
    i = 0
    try:
        while True:
            driver.push_frame(frame)
            i += 1
    except KeyboardInterrupt:
        pass
    finally:
        driver.stop()

from matrix.display_driver.arduino import Driver
from matrix.emulator.display import Display
import numpy as np
from time import sleep


def main():
    display = Display("emu1")
    display.start()
    driver = Driver((5, 6), display.port, 9600)
    driver.start()
    frame = np.array([[1, 1, 0, 1, 0],
                      [0, 0, 1, 1, 0],
                      [0, 1, 0, 1, 1],
                      [0, 0, 0, 1, 0],
                      [0, 1, 0, 1, 0],
                      [0, 0, 0, 1, 0]])
    i = 0
    try:
        while True:
            driver.push_frame(frame)
            sleep(1)
            i += 1
    except KeyboardInterrupt:
        print("Bye")
    finally:
        driver.stop()
        display.stop()

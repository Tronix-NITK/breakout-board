from matrix.display_driver.arduino import Driver
from matrix.emulator.display import Display
import numpy as np
from time import sleep


def main():
    display_emu = Display("emu1", (5, 7), scale=100)
    display_emu.start()
    driver = Driver((5, 7), display_emu.port, 9600)
    driver.start()
    frame = np.array([[0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0]])
    try:
        while True:
            driver.push_frame(frame)
            sleep(.1)
    except KeyboardInterrupt:
        print("Bye")
    finally:
        driver.stop()
        display_emu.stop()

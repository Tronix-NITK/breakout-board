from ..display_driver.arduino import Driver
from ..emulator import Display
import numpy as np
from time import sleep


def main():
    display_emu = Display("emu1", (6, 14), scale=50)
    display_emu.start()
    driver = Driver((6, 14), display_emu.port, 9600)
    driver.start()
    frame = np.array([
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
    ])
    try:
        while True:
            driver.push_frame(frame)
            sleep(.1)
    except KeyboardInterrupt:
        print("Bye")
    finally:
        driver.stop()
        display_emu.stop()

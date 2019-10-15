from ..display_driver.arduino import Driver
from ..arduino_emulator import Display
from ..game import Game
import numpy as np
from time import sleep
import cv2


def main():
    main2()


def main1():
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


def main2():
    render_wh = 200, 200
    down_sample_multi = 0.5
    frame_wh = int(render_wh[0] * down_sample_multi), int(render_wh[1] * down_sample_multi)
    display_emu = Display("emu1", frame_wh, scale=int(1 / down_sample_multi))
    display_emu.start()
    driver = Driver(frame_wh, display_emu.port, 9600)
    driver.start()

    def pusher(frame):
        frame = cv2.resize(frame, (0, 0), fx=down_sample_multi, fy=down_sample_multi, interpolation=cv2.INTER_NEAREST)
        driver.push_frame(frame)

    game = Game(render_wh)
    game.push_frame = pusher
    game.start()
    try:
        while True:
            game.tick()
            sleep(0.01)
    except KeyboardInterrupt:
        print("Bye")
    finally:
        game.stop()
        driver.stop()
        display_emu.stop()

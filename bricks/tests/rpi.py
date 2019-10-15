from ..display_driver.rpi import Driver
from ..game import Game
import numpy as np
from time import sleep
import cv2


def main():
    main2()


def main1():
    driver = Driver((6, 14), (17, 27, 22))
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
    except KeyboardInterrupt:
        print("Bye")
    finally:
        driver.stop()


def main2():
    render_wh = 6*50, 14*50
    down_sample_multi = 1/50
    frame_wh = int(render_wh[0] * down_sample_multi), int(render_wh[1] * down_sample_multi)
    driver = Driver(frame_wh, (17, 27, 22))
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

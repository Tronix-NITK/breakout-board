import os
import pty
import cv2
from threading import Thread
import serial
import numpy as np
from math import ceil


def _bin_array(val, m):
    return np.array(list(np.binary_repr(val, m))).astype(np.int8)


class Display:
    def __init__(self, name, resolution, scale=1):
        self.name = name
        self.resolution = resolution
        self.scale = scale
        self._thread = None
        self._run_flag = False
        self._master = None
        self.port = None
        self._col_len = 1
        self._val_len = ceil(resolution[1] / 8)

    def start(self):
        self._master, slave = pty.openpty()
        self.port = os.ttyname(slave)
        self._run_flag = True
        self._thread = Thread(target=self._run)
        self._thread.start()

    def stop(self):
        self._run_flag = False
        ser = serial.Serial(self.port, 9600)
        ser.write(b"close")
        ser.close()
        self._thread.join()
        cv2.destroyWindow(self.name)

    def _run(self):
        w, h = self.resolution
        frame = np.zeros((h, w))
        while self._run_flag:
            data = os.read(self._master, 1000)
            if not self._run_flag:
                break
            col = int.from_bytes(data[:self._col_len], byteorder='big')
            val = int.from_bytes(data[self._col_len:], byteorder='big')
            frame[:, col] = _bin_array(val, h)
            if col == w - 1:
                cv2.imshow(self.name, cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale))
                cv2.waitKey(1)
            os.write(self._master, b"\0")

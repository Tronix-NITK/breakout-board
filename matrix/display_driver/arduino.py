from matrix.display_driver.driver import Driver as DriverBase

import serial
import numpy as np
from math import ceil


class Driver(DriverBase):
    def __init__(self, resolution, port, baud_rate):
        self._serial_dev = serial.Serial()
        self._serial_dev.port = port
        self._serial_dev.baudrate = baud_rate
        _, h = resolution
        self._reduction_matrix = np.array([2 ** i for i in range(h)])
        self._col_len = 1
        self._val_len = ceil(h / 8)

    def start(self):
        self._serial_dev.open()

    def stop(self):
        self._serial_dev.close()

    def push_frame(self, frame):
        for col, val in enumerate(self._reduction_matrix.dot(frame)):
            data = col.to_bytes(self._col_len, "big") + int(val).to_bytes(self._val_len, "big")
            self._serial_dev.write(data)
            self._serial_dev.read(1)

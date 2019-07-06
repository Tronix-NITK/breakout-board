import os
import pty
import cv2
from threading import Thread
import serial


class Display:
    def __init__(self, name):
        self.name = name
        self._thread = None
        self._run_flag = False
        self._master = None
        self.port = None

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
        # cv2.destroyWindow(self.name)

    def _run(self):
        while self._run_flag:
            data = os.read(self._master, 1000)
            if not self._run_flag:
                break
            os.write(self._master, b"\0")
            print(list(map(int, data)))

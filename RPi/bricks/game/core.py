import numpy as np
import threading


class Game:
    def __init__(self, world_shape):
        self.world_shape = world_shape
        self.world_h, self.world_w = world_shape
        self.frame = np.zeros(self.world_shape)
        self.collision_matrix = np.zeros(self.world_shape)

        self.stop_called = False

        self.bat_pos = self.world_w // 2

    def start(self):
        pass

    def run(self):
        while not self.stop_called:
            pass

    def input_cmd(self, cmd):
        pass

    def input_move_to(self, pos):
        self.bat_pos = pos * self.world_w

    def stop(self):
        self.stop_called = True

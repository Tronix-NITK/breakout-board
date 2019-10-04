import numpy as np
import cv2
from typing import Tuple

from RPi.bricks.game.PhyEngine import PhyEngineNode
import RPi.bricks.game.RenderEngine as Re
import RPi.bricks.game.PhyEngine as Pe


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


class Brick(Re.Rect.LogicNode, Pe.StaticNode.LogicNode):
    def __init__(self, xy, wh):
        super().__init__()
        self.x, self.y = xy
        self.w, self.h = wh

    def get_hitbox(self):
        return self.x, self.y, self.w, self.h

    def get_xy(self):
        return self.x, self.y

    def get_wh(self):
        return self.w, self.h

    def on_hit(self, node: PhyEngineNode.LogicNode):
        print("HIT")


class Ball(Re.SolidRect.LogicNode, Pe.DynamicNode.LogicNode):
    def __init__(self, xy, wh):
        super().__init__()
        self.x, self.y = xy
        self.w, self.h = wh

    def get_hitbox(self):
        return self.x, self.y, self.w, self.h

    def get_xy(self):
        return self.x, self.y

    def get_wh(self):
        return self.w, self.h

    def on_hit(self, node: PhyEngineNode.LogicNode):
        print("HIT")

    def on_move(self, xy: Tuple[int, int]):
        self.x, self.y = xy


def main():
    re = Re.RenderEngine((150, 150), (500, 500))
    pe = Pe.PhyEngine()
    bricks = [
        Brick((10, 10), (10, 130)),
        Brick((10, 10), (130, 10)),
        Brick((130, 10), (10, 130)),
        Brick((10, 130), (130, 10)),
        Brick((30, 43), (10, 20)),
        Brick((63, 93), (30, 20)),
        Brick((75, 40), (50, 5)),
    ]
    for b in bricks:
        re.link_node(b)
        pe.link_node(b)
    b = Ball((20, 20), (10, 10))
    re.link_node(b)
    pe.link_node(b)
    run = True
    pe.apply_boost(b, (-1, 1))
    while run:
        pe.tick()
        cv2.imshow("win", re.tick())
        run = (cv2.waitKey(10) != ord("q"))


if __name__ == '__main__':
    main()

import numpy as np
import cv2
from typing import Tuple
from random import randint

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


class Boundary(Pe.StaticNode.LogicNode):
    def __init__(self, xy, wh):
        super().__init__()
        self.x, self.y = xy
        self.w, self.h = wh

    def get_hitbox(self):
        return self.x, self.y, self.w, self.h

    def on_hit(self, node: PhyEngineNode.LogicNode):
        pass


class Brick(Re.Rect.LogicNode, Pe.StaticNode.LogicNode):
    destroy = None

    def __init__(self, xy, wh):
        super().__init__()
        self.x, self.y = xy
        self.w, self.h = wh

    def get_hitbox(self):
        return self.x, self.y, self.w, self.h

    def get_corner(self):
        return self.x, self.y

    def get_shape(self):
        return self.w, self.h

    def on_hit(self, node: PhyEngineNode.LogicNode):
        Brick.destroy(self)


class Ball(Re.SolidCircle.LogicNode, Pe.DynamicNode.LogicNode):
    def __init__(self, xy, r):
        super().__init__()
        self.x, self.y = xy
        self.r = r

    def get_hitbox(self):
        return self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r

    def get_center(self):
        return self.x, self.y

    def get_radius(self):
        return self.r

    def on_hit(self, node: PhyEngineNode.LogicNode):
        pass

    def on_move(self, dxy: Tuple[int, int]):
        self.x, self.y = self.x + dxy[0], self.y + dxy[1]


def main():
    world_w, world_h = 500, 500
    re = Re.RenderEngine((world_w, world_h))
    pe = Pe.PhyEngine()

    def destroy(o):
        re.unlink_node(o)
        pe.unlink_node(o)

    Brick.destroy = destroy
    boundary_width = 10
    boundaries = (
        Boundary((-boundary_width, -boundary_width), (world_w + 2 * boundary_width, boundary_width)),
        Boundary((world_w, -boundary_width), (boundary_width, world_h + 2 * boundary_width)),
        Boundary((-boundary_width, world_h), (world_w + 2 * boundary_width, boundary_width)),
        Boundary((-boundary_width, -boundary_width), (boundary_width, world_h + 2 * boundary_width)),
    )
    bricks = (
        Brick(rand_point(500, 500), rand_point(100, 100))
        for _ in range(20)
    )
    ball = Ball((200, 200), 15)
    for b in boundaries:
        pe.link_node(b)
    for b in bricks:
        re.link_node(b)
        pe.link_node(b)
    re.link_node(ball)
    pe.link_node(ball)
    run = True
    pe.apply_boost(ball, (-5, 10))
    while run:
        pe.tick()
        cv2.imshow("win", re.tick())
        run = (cv2.waitKey(10) != ord("q"))


def rand_point(w, h):
    return randint(20, w), randint(20, h)


if __name__ == '__main__':
    main()

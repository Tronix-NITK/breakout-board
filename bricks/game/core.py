import numpy as np
from typing import Tuple
from random import randint, sample

from bricks.game.PhyEngine import PhyEngineNode
import bricks.game.RenderEngine as Re
import bricks.game.PhyEngine as Pe


class Game:
    def __init__(self, world_shape):
        self.world_shape = world_shape
        self.world_h, self.world_w = world_shape
        self.frame = np.zeros(self.world_shape)
        self.collision_matrix = np.zeros(self.world_shape)

        self.stop_called = False

        self.bat_pos = self.world_w // 2
        self.re, self.pe = None, None

        self.ball = None
        self.push_frame = None

    def start(self):
        self.re = Re.RenderEngine((self.world_w, self.world_h))
        self.pe = Pe.PhyEngine()

        def destroy(o):
            self.re.unlink_node(o)
            self.pe.unlink_node(o)

        Brick.destroy = destroy
        boundary_width = 10
        boundaries = (
            Boundary((-boundary_width, -boundary_width), (self.world_w + 2 * boundary_width, boundary_width)),
            Boundary((self.world_w, -boundary_width), (boundary_width, self.world_h + 2 * boundary_width)),
            Boundary((-boundary_width, self.world_h), (self.world_w + 2 * boundary_width, boundary_width)),
            Boundary((-boundary_width, -boundary_width), (boundary_width, self.world_h + 2 * boundary_width)),
        )
        bricks = []
        y = 0
        for i in range(5):
            min_h, max_h = int(.05 * self.world_h), int(.1 * self.world_h)
            min_w = int(.1 * self.world_w)
            min_n, max_n = 4, 6
            n = randint(min_n, max_n)
            extra = self.world_w - min_w * n
            extras = [0] + sorted(sample(range(1, extra), n - 1)) + [extra]
            x = 0
            h = randint(min_h, max_h)
            for j in range(n):
                w = min_w + extras[j + 1] - extras[j]
                bricks.append(Brick((x, y), (w, h), 100 * w // self.world_w))
                x += w
            y += h

        ball = Ball((self.world_w * 50 // 100, self.world_h * 70 // 100), self.world_w * 3 // 100)
        for b in boundaries:
            self.pe.link_node(b)
        for b in bricks:
            self.re.link_node(b)
            self.pe.link_node(b)
        self.re.link_node(ball)
        self.pe.link_node(ball)
        self.pe.apply_boost(ball, (-8, -10))
        self.ball = ball

    def tick(self):
        self.pe.tick()
        self.push_frame(self.re.tick())

    def input_cmd(self, cmd):
        pass

    def input_move_to(self, pos):
        self.bat_pos = pos * self.world_w

    def stop(self):
        self.stop_called = True
        self.pe = self.re = None


class Boundary(Pe.StaticNode.LogicNode):
    def __init__(self, xy, wh):
        super().__init__()
        self.x, self.y = xy
        self.w, self.h = wh

    def get_hitbox(self):
        return self.x, self.y, self.w, self.h

    def on_hit(self, node: PhyEngineNode.LogicNode):
        pass


class Brick(Re.SolidRect.LogicNode, Pe.StaticNode.LogicNode):
    destroy = None
    border = 2

    def __init__(self, xy, wh, worth):
        super().__init__()
        self.x, self.y = xy
        self.w, self.h = wh
        self.worth = worth

    def get_hitbox(self):
        return self.x, self.y, self.w, self.h

    def get_corner(self):
        return self.x + self.border, self.y + self.border

    def get_shape(self):
        return self.w - 2 * self.border, self.h - 2 * self.border

    def on_hit(self, node: PhyEngineNode.LogicNode):
        Brick.destroy(self)


class Ball(Re.SolidCircle.LogicNode, Pe.DynamicNode.LogicNode):
    def __init__(self, xy, r):
        super().__init__()
        self.x, self.y = xy
        self.r = r
        self.score = 0

    def get_hitbox(self):
        return self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r

    def get_center(self):
        return self.x, self.y

    def get_radius(self):
        return self.r

    def on_hit(self, node: PhyEngineNode.LogicNode):
        if isinstance(node, Brick):
            self.score += node.worth
            print("Score", self.score)

    def on_move(self, dxy: Tuple[int, int]):
        self.x, self.y = self.x + dxy[0], self.y + dxy[1]

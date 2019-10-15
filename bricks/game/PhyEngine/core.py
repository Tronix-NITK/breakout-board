from __future__ import annotations
import abc
from typing import List, Optional, Tuple, Dict


class IDStore:
    def __init__(self):
        self._counter = 0

    def gen(self) -> int:
        self._counter += 1
        return self._counter


class PhyEngineNode(abc.ABC):
    class LogicNode(abc.ABC):
        def __init__(self):
            self.pe_id = None
            self.pe_node: Optional[PhyEngineNode] = None

        @staticmethod
        @abc.abstractmethod
        def factory_pe_node() -> PhyEngineNode:
            pass

        @abc.abstractmethod
        def get_hitbox(self):
            pass

        @abc.abstractmethod
        def on_hit(self, node: PhyEngineNode.LogicNode):
            pass

    def __init__(self):
        self.pe_id = None
        self.logic_node: Optional[PhyEngineNode.LogicNode] = None


class StaticNode(PhyEngineNode):
    class LogicNode(PhyEngineNode.LogicNode, abc.ABC):
        @staticmethod
        def factory_pe_node():
            return StaticNode()


class DynamicNode(PhyEngineNode):
    class LogicNode(PhyEngineNode.LogicNode, abc.ABC):
        @staticmethod
        def factory_pe_node():
            return DynamicNode()

        @abc.abstractmethod
        def on_move(self, xy: Tuple[int, int]):
            pass

    def __init__(self):
        super().__init__()
        self.vx, self.vy = 0, 0
        self.pe_px, self.pe_py = self.pe_x, self.pe_y = 0, 0

    def on_link(self):
        self.pe_px, self.pe_py = self.pe_x, self.pe_y = self.logic_node.get_hitbox()[:2]

    def sync(self):
        if (self.pe_x, self.pe_y) != self.logic_node.get_hitbox()[:2]:
            self.logic_node.on_move((self.vx, self.vy))


class PhyEngine:
    def __init__(self):
        self.id_store = IDStore()
        self.static_nodes: List[StaticNode] = []
        self.dynamic_nodes: List[DynamicNode] = []
        self.map: Dict[int, PhyEngineNode] = {}

    def link_node(self, logic_node: PhyEngineNode.LogicNode):
        pe_node = logic_node.factory_pe_node()
        pe_id = pe_node.pe_id = logic_node.pe_id = self.id_store.gen()
        logic_node.pe_node = pe_node
        pe_node.logic_node = logic_node
        self.map[pe_id] = pe_node
        if isinstance(pe_node, StaticNode):
            self.static_nodes.append(pe_node)
        elif isinstance(pe_node, DynamicNode):
            self.dynamic_nodes.append(pe_node)
            pe_node.on_link()

    def unlink_node(self, logic_node: PhyEngineNode.LogicNode):
        pe_id = logic_node.pe_id
        pe_node = self.map.pop(pe_id)
        if isinstance(pe_node, StaticNode):
            self.static_nodes.remove(pe_node)
        elif isinstance(pe_node, DynamicNode):
            self.dynamic_nodes.remove(pe_node)

    def tick(self):
        for node in self.dynamic_nodes:
            if node.vx != 0 or node.vy != 0:
                node.pe_px, node.pe_py = node.pe_x, node.pe_y
                node.pe_x += node.vx
                node.pe_y += node.vy
                hit_comp = self.check_col(node)
                if any(hit_comp):
                    mx, my = 1, 1
                    if hit_comp[1] or hit_comp[3]:
                        mx = -1
                    elif hit_comp[0] or hit_comp[2]:
                        my = -1
                    node.pe_x -= node.vx
                    node.pe_y -= node.vy
                    node.vx = mx * node.vx
                    node.vy = my * node.vy
                    node.pe_x += node.vx
                    node.pe_y += node.vy
                node.sync()

    def apply_boost(self, logic_node: DynamicNode.LogicNode, v: Tuple[int, int]):
        pe_node = self.map.get(logic_node.pe_id)
        assert pe_node is not None, "Logical node has no mapping"
        pe_node.vx, pe_node.vy = v

    def check_col(self, d_node: DynamicNode):
        _, _, w, h = d_node.logic_node.get_hitbox()
        x, y = d_node.pe_x, d_node.pe_y
        px, py = d_node.pe_px, d_node.pe_py
        d_node_hb = x, y, w, h
        lines = [
            LineSegment((x, y), (px, py)),
            LineSegment((x + w, y), (px + w, py)),
            LineSegment((x + w, y + h), (px + w, py + h)),
            LineSegment((x, y + h), (px, py + h)),
        ]
        impact = [0, 0, 0, 0]
        for s_node in self.static_nodes:
            hit, td, ts = _rect_overlapping(d_node_hb, s_node.logic_node.get_hitbox())
            if not hit:
                continue
            segments = _rect_to_line_segments(s_node.logic_node.get_hitbox())
            if LineSegment.intersecting(lines[0], segments[1]):
                impact[3] = 1
            elif LineSegment.intersecting(lines[0], segments[2]):
                impact[0] = 1
            elif LineSegment.intersecting(lines[1], segments[3]):
                impact[1] = 1
            elif LineSegment.intersecting(lines[1], segments[2]):
                impact[0] = 1
            elif LineSegment.intersecting(lines[2], segments[0]):
                impact[2] = 1
            elif LineSegment.intersecting(lines[2], segments[3]):
                impact[1] = 1
            elif LineSegment.intersecting(lines[3], segments[0]):
                impact[2] = 1
            elif LineSegment.intersecting(lines[3], segments[1]):
                impact[3] = 1
            else:
                continue
            s_node.logic_node.on_hit(d_node.logic_node)
        return tuple(impact)


def _rect_overlapping(r1: Tuple[int, int, int, int], r2: Tuple[int, int, int, int]):
    t1 = tuple(int(_point_in_rect(pt, r2)) for pt in _rect_to_points(r1))
    t2 = tuple(int(_point_in_rect(pt, r1)) for pt in _rect_to_points(r2))
    return (any(t1) or any(t2)), t1, t2


def _rect_to_points(r: Tuple[int, int, int, int]):
    x, y, w, h = r
    return (x, y), (x + w, y), (x + w, y + h), (x, y + h)


def _point_in_rect(pt: Tuple[int, int], r: Tuple[int, int, int, int]):
    px, py = pt
    x, y, w, h = r
    return x <= px <= (x + w) and y <= py <= (y + h)


class LineSegment:
    def __init__(self, p1, p2):
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2
        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1

    # def x(self, y: int) -> int:
    #     if self.dx == 0 and self.dy == 0:
    #         return self.x1 if y == self.y1 else None
    #     if self.dx == 0:
    #         return self.x1
    #     if self.dy == 0:
    #         return None
    #     return int(self.x1 + (y - self.y1) * self.dx / self.dy)
    #
    # def y(self, x: int) -> int:
    #     if self.dx == 0 and self.dy == 0:
    #         return self.y1 if x == self.x1 else None
    #     if self.dy == 0:
    #         return self.y1
    #     if self.dx == 0:
    #         return None
    #     return int(self.y1 + (x - self.x1) * self.dy / self.dx)

    @staticmethod
    def intersecting(l1: LineSegment, l2: LineSegment) -> bool:
        x1, y1, x2, y2 = l1.x1, l1.y1, l1.x2, l1.y2
        x3, y3, x4, y4 = l2.x1, l2.y1, l2.x2, l2.y2
        n_ta = (y3 - y4) * (x1 - x3) + (x4 - x3) * (y1 - y3)
        d_ta = (x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3)
        n_tb = (y1 - y2) * (x1 - x3) + (x2 - x1) * (y1 - y3)
        d_tb = (x4 - x3) * (y1 - y2) - (x1 - x2) * (y4 - y3)
        return 0 <= n_ta <= d_ta and 0 <= n_tb <= d_tb


def _rect_to_line_segments(rect: Tuple[int, int, int, int]):
    x, y, w, h = rect
    return (
        LineSegment((x, y), (x + w, y)),
        LineSegment((x + w, y), (x + w, y + h)),
        LineSegment((x + w, y + h), (x, y + h)),
        LineSegment((x, y + h), (x, y)),
    )

from __future__ import annotations
import abc
import numpy as np
import cv2
from typing import List, Optional


class IDStore:
    def __init__(self):
        self._counter = 0

    def gen(self) -> int:
        self._counter += 1
        return self._counter


class RenderEngineNode(abc.ABC):
    class LogicNode(abc.ABC):
        def __init__(self):
            self.re_id = None
            self.re_node: Optional[RenderEngineNode] = None

        @staticmethod
        @abc.abstractmethod
        def factory_re_node() -> RenderEngineNode:
            pass

    def __init__(self):
        self.re_id = None
        self.logic_node: Optional[RenderEngineNode.LogicNode] = None


class SolidRect(RenderEngineNode):
    class LogicNode(RenderEngineNode.LogicNode, abc.ABC):
        @staticmethod
        def factory_re_node():
            return SolidRect()

        @abc.abstractmethod
        def get_xy(self):
            pass

        @abc.abstractmethod
        def get_wh(self):
            pass

    def __init__(self):
        super().__init__()


class Rect(RenderEngineNode):
    class LogicNode(RenderEngineNode.LogicNode):
        @staticmethod
        def factory_re_node():
            return Rect()

        @abc.abstractmethod
        def get_xy(self):
            pass

        @abc.abstractmethod
        def get_wh(self):
            pass

    def __init__(self):
        super().__init__()


class RenderEngine:
    def __init__(self, world_wh, frame_wh):
        self.id_store = IDStore()
        self.world_w, self.world_h = world_wh
        self.frame_w, self.frame_h = frame_wh
        self.frame = np.zeros(frame_wh)
        self.nodes: List[RenderEngineNode] = []

    def link_node(self, logic_node: RenderEngineNode.LogicNode):
        re_node = logic_node.factory_re_node()
        re_id = re_node.re_id = logic_node.re_id = self.id_store.gen()
        logic_node.re_node = re_node
        re_node.logic_node = logic_node
        self.nodes.append(re_node)

    def _render(self):
        for node in self.nodes:
            if isinstance(node, SolidRect):
                x, y = node.logic_node.get_xy()
                w, h = node.logic_node.get_wh()
                pt1 = self._translate_point((x, y))
                pt2 = self._translate_point((x + w, y + h))
                cv2.rectangle(self.frame, pt1, pt2, 1, cv2.FILLED)
            elif isinstance(node, Rect):
                x, y = node.logic_node.get_xy()
                w, h = node.logic_node.get_wh()
                pt1 = self._translate_point((x, y))
                pt2 = self._translate_point((x + w, y + h))
                cv2.rectangle(self.frame, pt1, pt2, 1)

    def tick(self) -> np.array:
        self.frame.fill(0)
        self._render()
        return self.frame

    def _translate_point(self, pt):
        x, y = pt
        return int(x * self.frame_w / self.world_w), int(y * self.frame_h / self.world_h)

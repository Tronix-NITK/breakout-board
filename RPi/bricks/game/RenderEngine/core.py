from __future__ import annotations
import abc
import numpy as np
import cv2
from typing import List, Optional, Dict


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

    @abc.abstractmethod
    def render(self, frame):
        pass


class SolidRect(RenderEngineNode):
    class LogicNode(RenderEngineNode.LogicNode, abc.ABC):
        @staticmethod
        def factory_re_node():
            return SolidRect()

        @abc.abstractmethod
        def get_corner(self):
            pass

        @abc.abstractmethod
        def get_shape(self):
            pass

    def __init__(self):
        super().__init__()

    def render(self, frame):
        x, y = self.logic_node.get_corner()
        w, h = self.logic_node.get_shape()
        cv2.rectangle(frame, (x, y), (x + w, y + h), 1, cv2.FILLED)
        return frame


class Rect(RenderEngineNode):
    class LogicNode(RenderEngineNode.LogicNode):
        @staticmethod
        def factory_re_node():
            return Rect()

        @abc.abstractmethod
        def get_corner(self):
            pass

        @abc.abstractmethod
        def get_shape(self):
            pass

    def __init__(self):
        super().__init__()

    def render(self, frame):
        x, y = self.logic_node.get_corner()
        w, h = self.logic_node.get_shape()
        cv2.rectangle(frame, (x, y), (x + w, y + h), 1)
        return frame


class SolidCircle(RenderEngineNode):
    class LogicNode(RenderEngineNode.LogicNode):
        @staticmethod
        def factory_re_node():
            return SolidCircle()

        @abc.abstractmethod
        def get_center(self):
            pass

        @abc.abstractmethod
        def get_radius(self):
            pass

    def __init__(self):
        super().__init__()

    def render(self, frame):
        cv2.circle(frame, self.logic_node.get_center(),
                   self.logic_node.get_radius(), 1, cv2.FILLED)
        return frame


class RenderEngine:
    def __init__(self, world_wh):
        self.id_store = IDStore()
        self.world_w, self.world_h = world_wh
        self.frame = np.zeros(world_wh)
        self.nodes: List[RenderEngineNode] = []
        self.map: Dict[int, RenderEngineNode] = {}

    def link_node(self, logic_node: RenderEngineNode.LogicNode):
        re_node = logic_node.factory_re_node()
        re_id = re_node.re_id = logic_node.re_id = self.id_store.gen()
        logic_node.re_node = re_node
        re_node.logic_node = logic_node
        self.nodes.append(re_node)
        self.map[re_id] = re_node

    def unlink_node(self, logic_node: RenderEngineNode.LogicNode):
        re_id = logic_node.re_id
        re_node = self.map.pop(re_id)
        self.nodes.remove(re_node)

    def _render(self):
        for node in self.nodes:
            self.frame = node.render(self.frame)

    def tick(self) -> np.array:
        self.frame.fill(0)
        self._render()
        return self.frame

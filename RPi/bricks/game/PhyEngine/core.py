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
        def on_hit(self, node: PhyEngineNode.LogicNode):
            pass

    def __init__(self):
        self.pe_id = None
        self.logic_node: Optional[PhyEngineNode.LogicNode] = None

    @staticmethod
    @abc.abstractmethod
    def is_static() -> bool:
        pass


class StaticNode(PhyEngineNode):
    class LogicNode(PhyEngineNode.LogicNode, abc.ABC):
        @staticmethod
        def factory_pe_node():
            return StaticNode()

        @abc.abstractmethod
        def get_xy(self):
            pass

        @abc.abstractmethod
        def get_wh(self):
            pass

    @staticmethod
    def is_static():
        return True


class DynamicNode(PhyEngineNode):
    class LogicNode(PhyEngineNode.LogicNode, abc.ABC):
        @staticmethod
        def factory_pe_node():
            return DynamicNode()

        @abc.abstractmethod
        def get_xy(self):
            pass

        @abc.abstractmethod
        def get_wh(self):
            pass

        @abc.abstractmethod
        def on_move(self, xy: Tuple[int, int]):
            pass

    @staticmethod
    def is_static():
        return False

    def __init__(self):
        super().__init__()
        self.vx, self.vy = 0, 0
        self.pe_px, self.pe_py = self.pe_x, self.pe_y = 0, 0

    def on_link(self):
        self.pe_px, self.pe_py = self.pe_x, self.pe_y = self.logic_node.get_xy()

    def sync(self):
        if (self.pe_x, self.pe_y) != self.logic_node.get_xy():
            self.logic_node.on_move((self.pe_x, self.pe_y))


class PhyEngine:
    def __init__(self):
        self.id_store = IDStore()
        self.static_nodes: List[StaticNode] = []
        self.dynamic_nodes: List[DynamicNode] = []
        self.dynamic_map: Dict[int, DynamicNode] = {}

    def link_node(self, logic_node: PhyEngineNode.LogicNode):
        pe_node = logic_node.factory_pe_node()
        pe_id = pe_node.pe_id = logic_node.pe_id = self.id_store.gen()
        logic_node.pe_node = pe_node
        pe_node.logic_node = logic_node
        if isinstance(pe_node, StaticNode):
            self.static_nodes.append(pe_node)
        elif isinstance(pe_node, DynamicNode):
            self.dynamic_nodes.append(pe_node)
            self.dynamic_map[pe_id] = pe_node
            pe_node.on_link()

    def tick(self):
        for node in self.dynamic_nodes:
            if node.vx != 0 or node.vy != 0:
                node.pe_px, node.pe_py = node.pe_x, node.pe_y
                node.pe_x += node.vx
                node.pe_y += node.vy
                node.sync()

    def apply_boost(self, logic_node: DynamicNode.LogicNode, v: Tuple[int, int]):
        pe_node = self.dynamic_map.get(logic_node.pe_id)
        assert pe_node is not None, "Logical node has no mapping"
        pe_node.vx, pe_node.vy = v

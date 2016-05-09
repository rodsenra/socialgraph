# -*- coding: utf-8 -*-


class Graph(object):
    def __init__(self):
        self._nodes = {}

    def add_edge(self, src, dst):
        try:
            src_node = self._nodes[src]
        except KeyError:
            src_node = self._nodes[src] = Node(src)

        try:
            dst_node = self._nodes[dst]
        except KeyError:
            dst_node = self._nodes[dst] = Node(dst)

        src_node.link(dst_node)
        dst_node.linked(src_node)


class Node(object):
    def __init__(self, node_id):
        self.id = node_id
        self._pow = {self.id: 1}
        self._order = [node_id]
        self._adj = []

    def full_power(self):
        return [(i, self._pow[i]) for i in self._order]

    def current_power(self):
        last_id = self._order[-1]
        return self._pow[last_id]

    def power_from(self, node_id):
        return self._pow[node_id]

    def power_before(self, node_id):
        target_index = self._order.index(node_id) - 1
        if target_index >= 0:
            target_id = self._order[target_index]
            return self._pow[target_id]

    def link(self, to_node):
        self._adj.append(to_node.id)

    def linked(self, from_node):
        if from_node.id not in self._adj:
            self._pow[from_node.id] = self.current_power() + from_node.current_power()
        else:
            external_power = from_node.current_power() - from_node.power_from(self.id) + from_node.power_before(self.id)
            self._pow[from_node.id] = self.current_power() + external_power
        self._order.append(from_node.id)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test some edge cases.
"""

import unittest
import networkx as nx
from socialgraph import socialgraph


class TestGraphWithCicles(unittest.TestCase):

    def setUp(self):
        self.G = nx.DiGraph()
        self.G.add_edge('a', 'b', topic='dummy')
        self.G.add_edge('b', 'c', topic='dummy')
        self.G.add_edge('c', 'a', topic='dummy')
        self.G.add_edge('f', 'd', topic='dummy')
        self.G.add_edge('d', 'e', topic='dummy')

    def tearDown(self):
        del self.G

    def test_calc_committee(self):
        committee = socialgraph.elect_committee(self.G, 2)
        self.assertEquals(['a', 'e'], committee.keys())
        self.assertEquals(committee['a'], ['a', 'c', 'b'])
        self.assertEqual(committee['e'], ['e', 'd', 'f'])


class TestGraphWithoutCicles(unittest.TestCase):

    def setUp(self):
        self.G = nx.DiGraph()
        self.G.add_edge('c', 'b', topic='dummy')
        self.G.add_edge('b', 'a', topic='dummy')
        self.G.add_edge('x', 'a', topic='dummy')
        self.G.add_edge('x', 'b', topic='dummy')
        self.G.add_edge('x', 'c', topic='dummy')

    def tearDown(self):
        del self.G

    def test_calc_committee(self):
        committee = socialgraph.elect_committee(self.G, 1)
        self.assertEquals(['a'], committee.keys())
        self.assertEquals(committee['a'], ['a', 'x', 'c', 'b'])

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())

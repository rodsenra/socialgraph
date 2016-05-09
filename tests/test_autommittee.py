#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test some edge cases.
"""

import unittest
from socialgraph import autommittee


class TestPowerHistory(unittest.TestCase):

    def setUp(self):
        self.G = autommittee.Graph()
        self.G.add_edge('b', 'a')
        self.G.add_edge('a', 'c')
        self.G.add_edge('d', 'c')
        self.G.add_edge('e', 'c')
        self.G.add_edge('c', 'a')

    def tearDown(self):
        del self.G

    def test_calc_power(self):
        self.assertEqual([('a', 1), ('b', 2), ('c', 5)], self.G._nodes['a'].full_power())
        self.assertEqual([('c', 1), ('a', 3), ('d', 4), ('e', 5)], self.G._nodes['c'].full_power())
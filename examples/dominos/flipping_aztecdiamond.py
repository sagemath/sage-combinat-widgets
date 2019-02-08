#!/usr/bin/env python
# coding: utf-8

from sage.graphs.graph import Graph
from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter

class DominoGeometry:
    r"""
    The geometry of the domino."""
    def __init__(self, first, second):
        """A domino is a pair of pairs"""
        self.first = first
        self.second = second
        self.direction = None
        self.orientation = None
        self.compute()

    def __str__(self):
        if self.value:
            return str(self.first) + ' -> ' + str(self.second) + " PRESSED"
        return str(self.first) + ' -> ' + str(self.second)

    def compute(self):
        r"""Compute domino direction and orientation."""
        if self.first[0] == self.second[0]: # same row
            self.direction = 'horizontal'
            if self.first[1] + 1 == self.second[1]:
                self.orientation = 1 # left to right
            elif self.first[1] == self.second[1] + 1:
                self.orientation = -1 # right to left
        elif self.first[1] == self.second[1]: # same column
            self.direction = 'vertical'
            if self.first[0] + 1 == self.second[0]:
                self.orientation = 1 # top to bottom
            elif self.first[0] == self.second[0] + 1:
                self.orientation = -1 # bottom to top
        if self.orientation == 1:
            self.parity = (self.first[0]%2 + self.first[1]%2)%2
        elif self.orientation == -1:
            self.parity = (self.second[0]%2 + self.second[1]%2)%2

    def neighbors(self):
        r"""
        Return list of parallel neighbouring matches
        Note: we consider only horizontal or vertical matches"""
        if self.direction == 'horizontal':
            return [(((self.first[0] + 1, self.first[1]), (self.second[0] + 1, self.second[1]))),
                    (((self.first[0] - 1, self.first[1]), (self.second[0] - 1, self.second[1])))]
        else:
            return [(((self.first[0], self.first[1] + 1), (self.second[0], self.second[1] + 1))),
                    (((self.first[0], self.first[1] - 1), (self.second[0], self.second[1] - 1)))]

    def reverse(self):
        return DominoGeometry(self.second, self.first)

class FlippingAztecDiamond(Graph):
    def __init__(self, n, matching=()):
        try:
            assert n > 0 and n.is_integer()
        except:
            raise TypeException("We need a positive integer for the graph order.")
        N = 2 * n
        positions = ((i, j) for i in range(N) for j in range(N) if i - n <= j <= n + i and n - 1 - i <= j <= 3 * n - i - 1)
        super(FlippingAztecDiamond, self).__init__(name="Flipping Aztec Diamond Graph of order {}".format(n))
        self.add_vertices(positions)
        self.add_edges((pos,(pos[0],pos[1]+1)) for pos in positions if (pos[0],pos[1]+1) in positions)
        self.add_edges((pos,(pos[0]+1,pos[1])) for pos in positions if (pos[0]+1,pos[1]) in positions)
        try:
            for t in matching:
                assert (t[0][0] == t[1][0] and (t[0][1] + 1 == t[1][1] or t[0][1] == t[1][1] + 1) or \
                        t[0][1] == t[1][1] and (t[0][0] + 1 == t[1][0] or t[0][0] == t[1][0] + 1))
        except:
            raise TypeException("This matching is not suitable for a flipping aztec diamond (tuple {} is not valid)." . format(t))
        self.matching = matching # tuple with only horizontal or vertical consecutive matches
        #self.order = n # We have self.order() already

    def __copy__(self):
        return FlippingAztecDiamond.__init__(self.order(), self.matching)

    def domino_for_position(self, pos):
        try:
            assert type(pos) is type((0,))
            assert pos in self.vertices()
        except:
            raise TypeException("Argument `pos` must be a tuple and a graph vertex")
        for m in self.matching:
            if m[0] == pos:
                return DominoGeometry(pos, m[1])
            if m[1] == pos:
                return DominoGeometry(m[0], pos)

    def neighbors(self, m):
        r"""
        Return list of parallel neighbouring matches
        Note: we consider only horizontal or vertical matches"""
        try:
            assert m in self.matching
        except:
            raise Exception("Pair {} is not matched" . format(m))
        d = DominoGeometry(m[0], m[1])
        neighbors = []
        if d.direction == 'horizontal':
            if ((first[0]+1, first[1]), (second[0]+1, second[1])) in self.matching:
                neighbors.append(((first[0]+1, first[1]), (second[0]+1, second[1])))
            elif ((second[0]+1, second[1]), (first[0]+1, first[1])) in self.matching:
                neighbors.append(((second[0]+1, second[1]), (first[0]+1, first[1])))
            if ((first[0]-1, first[1]), (second[0]-1, second[1])) in self.matching:
                neighbors.append(((first[0]-1, first[1]), (second[0]-1, second[1])))
            elif ((second[0]-1, second[1]), (first[0]-1, first[1])) in self.matching:
                neighbors.append(((second[0]-1, second[1]), (first[0]-1, first[1])))
        else: # vertical
            if ((first[0], first[1]+1), (second[0], second[1]+1)) in self.matching:
                neighbors.append(((first[0], first[1]+1), (second[0], second[1]+1)))
            elif ((second[0], second[1]+1), (first[0], first[1]+1)) in self.matching:
                neighbors.append(((second[0], second[1]+1), (first[0], first[1]+1)))
            if ((first[0], first[1]-1), (second[0], second[1]-1)) in self.matching:
                neighbors.append(((first[0], first[1]-1), (second[0], second[1]-1)))
            elif ((second[0], second[1]-1), (first[0], first[1]-1)) in self.matching:
                neighbors.append(((second[0], second[1]-1), (first[0], first[1]-1)))
        return neighbors

class DominosAdapter(GraphGridViewAdapter):
    def set_cell(self, obj, pos, val=True, dirty={}):
        r"""
        When we click on a graph cell,
        we prepare a possible flip
        or we try to complete the flip if it has been prepared previously
        """
        #print(pos, val, dirty)
        # Find out the relevant matching for 'pos'
        d1 = obj.domino_for_position(pos)
        if dirty: # if i'm a neighbor, then flip and return a new obj ; else return an error
            # Consider the relevant matching(s)
            for p in dirty:
                d2 = obj.domino_for_position(p)
                if d2 in d1.neighbors():
                    return obj  # flip
            return Exception("Please select a second domino!")
        else: # return an error
            return Exception("Please select a second domino!")

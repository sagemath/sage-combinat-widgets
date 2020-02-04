#!/usr/bin/env python
# coding: utf-8

from sage.graphs.graph import Graph


class DominoGeometry:
    r"""
    The geometry of the domino."""
    def __init__(self, first, second):
        """A domino is a pair of pairs"""
        self.first = first
        self.second = second
        self.direction = None
        self.orientation = None
        self.index_for_display = None
        self.compute()

    def __repr__(self):
        return "DominoGeometry %s -> %s" % (self.first, self.second)

    def __eq__(self, other):
        assert issubclass(other.__class__, DominoGeometry)
        return self.first == other.first and self.second == other.second

    def __lt__(self, other):
        assert issubclass(other.__class__, DominoGeometry)
        if other.direction != self.direction:
            return False
        return (self.first < other.first and self.second < other.second) \
            or (self.first < other.second and self.second < other.first)

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
        self.index_for_display = self.calc_index_for_display()

    def calc_index_for_display(self):
        if self.direction == 'horizontal':
            if not self.parity:
                return 1
            else:
                return 2
        else:
            if not self.parity:
                return 3
            else:
                return 4

    def reverse(self):
        return DominoGeometry(self.second, self.first)

    def neighbors(self):
        r"""
        Return list of parallel neighbouring matches
        Note: we consider only horizontal or vertical matches"""
        if self.direction == 'horizontal':
            return [DominoGeometry((self.first[0] + 1, self.first[1]), (self.second[0] + 1, self.second[1])),
                    DominoGeometry((self.first[0] - 1, self.first[1]), (self.second[0] - 1, self.second[1]))]
        else:
            return [DominoGeometry((self.first[0], self.first[1] + 1), (self.second[0], self.second[1] + 1)),
                    DominoGeometry((self.first[0], self.first[1] - 1), (self.second[0], self.second[1] - 1))]

    def flip(self, other):
        """Flip self with some neighboring domino"""
        if self.orientation * other.orientation == 1: # Same orientation
            self.second, other.first = other.first, self.second
        else:
            self.second, other.second = other.second, self.second
        self.compute()
        other.compute()


class FlippingAztecDiamond(Graph):
    def __init__(self, n, matching=()):
        try:
            assert n > 0 and n.is_integer()
        except:
            raise TypeError("We need a positive integer for the graph order.")
        N = 2 * n
        positions = ((i, j) for i in range(N) for j in range(N) if i - n <= j <= n + i and n - 1 - i <= j <= 3 * n - i - 1)
        super(FlippingAztecDiamond, self).__init__(name="Flipping Aztec Diamond Graph of order {}".format(n))
        self.aztec_order = n
        self.add_vertices(positions)
        self.add_edges((pos,(pos[0],pos[1]+1)) for pos in positions if (pos[0],pos[1]+1) in positions)
        self.add_edges((pos,(pos[0]+1,pos[1])) for pos in positions if (pos[0]+1,pos[1]) in positions)
        try:
            for t in matching:
                assert (t[0][0] == t[1][0] and (t[0][1] + 1 == t[1][1] or t[0][1] == t[1][1] + 1) or \
                        t[0][1] == t[1][1] and (t[0][0] + 1 == t[1][0] or t[0][0] == t[1][0] + 1))
        except:
            raise TypeError("This matching is not suitable for a flipping aztec diamond (tuple {} is not valid)." . format(t))
        self.matching = self.apply_matching(matching) # dominos with only horizontal or vertical consecutive matches

    def __copy__(self):
        return FlippingAztecDiamond.__init__(self, self.aztec_order, ((m.first, m.second) for m in self.matching))

    def apply_matching(self, matching):
        self.matching = [DominoGeometry(t[0], t[1]) for t in matching]

    def domino_for_position(self, pos):
        try:
            assert type(pos) is type((0,))
            assert pos in self.vertices()
        except:
            raise TypeError("Argument `pos` must be a tuple and a graph vertex")
        for d in self.matching:
            if d.first == pos or d.second == pos:
                return d

    def position_for_domino(d):
        return d.first

    @staticmethod
    def flip(d1, d2):
        """d1 and d2 are dominos"""
        if d1==d2 or not d2 in d1.neighbors():
            return
        if d1 < d2:
            d1.flip(d2)
        else:
            d2.flip(d1)

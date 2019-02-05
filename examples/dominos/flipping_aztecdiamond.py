#!/usr/bin/env python
# coding: utf-8

from sage.graphs.graph import Graph

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
        self.order = n

    def neighbors(self, m):
        r"""
        Return list of parallel neighbouring matches
        Note: we consider only horizontal or vertical matches"""
        try:
            assert m in self.matching
        except:
            raise Exception("Pair {} is not matched" . format(m))
        first, second = m
        neighbors = []
        if first[0] == second[0]:  # horizontal
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

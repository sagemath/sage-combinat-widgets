# -*- coding: utf-8 -*-
r"""
Grid View Adapter for grid-representable graphs

**Grid View graphs operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GraphGridViewAdapter.compute_cells` | Compute graph cells as a dictionary { coordinate pair : label }
    :meth:`~GraphGridViewAdapter.from_cells` | Create a new graph from a cells dictionary
    :meth:`~GraphGridViewAdapter.addable_cells` | List addable cells
    :meth:`~GraphGridViewAdapter.removable_cells` | List removable cells
    :meth:`~GraphGridViewAdapter.add_cell` | Add a cell
    :meth:`~GraphGridViewAdapter.remove_cell` | Remove a cell
    :meth:`~GraphGridViewAdapter.append_row` | Append a row
    :meth:`~GraphGridViewAdapter.insert_row` | Insert a row at given index
    :meth:`~GraphGridViewAdapter.remove_row` | Remove a row at given index
    :meth:`~GraphGridViewAdapter.append_column` | Append a column
    :meth:`~GraphGridViewAdapter.insert_column` | Insert a column at given index
    :meth:`~GraphGridViewAdapter.remove_column` | Remove a column at given index
"""


from sage.all import Graph

class GraphGridViewAdapter(Graph):
    def compute_cells(self):
        r"""
        From the graph vertices,
        return a dictionary { coordinates pair : None }
        TESTS::
        sage: from sage.graphs.generators.families import AztecDiamondGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(AztecDiamondGraph(2))
        sage: ga.compute_cells()
        {(0, 1): None,
        (0, 2): None,
        (1, 0): None,
        (1, 1): None,
        (1, 2): None,
        (1, 3): None,
        (2, 0): None,
        (2, 1): None,
        (2, 2): None,
        (2, 3): None,
        (3, 1): None,
        (3, 2): None}
        """
        cells = {}
        for v in self.vertices():
            cells[v] = None
        return cells

    @staticmethod
    def from_cells(cells={}):
        r"""
        From a dictionary { coordinates pair : None }
        return a graph with one vertex for every coordinates pair
        TESTS:
        sage: from sage.graphs.generators.families import AztecDiamondGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter
        sage: ga.from_cells({(0, 0): None, (0, 1): None, (1, 0): None, (1, 1): None, (2, 0): None, (2, 1): None})
        Graph on 6 vertices
        """
        g = Graph()
        g.add_vertices(list(cells.keys()))
        return g

    def addable_cells(self):
        r"""
        No cell should be added in isolation
        except for linear graphs
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((2,3)))
        sage: ga.addable_cells()
        []
        sage: ga = GraphGridViewAdapter(GridGraph((1,3)))
        sage: ga.addable_cells()
        [(0, 3)]
        """
        if not self.num_verts():
            return [(0,0)]
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
            if row_max > 0 and col_max > 0:
                return []
        if row_max > 0:
            return [(row_max + 1, 0)]
        elif col_max > 0:
            return [(0, col_max + 1)]
        return [(0,1),(1,0)]

    def removable_cells(self):
        r"""
        No cell should be removed in isolation
        except for linear graphs
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((2,3)))
        sage: ga.removable_cells()
        []
        sage: ga = GraphGridViewAdapter(GridGraph((1,3)))
        sage: ga.removable_cells()
        [(0, 2)]
        """
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
            if row_max > 0 and col_max > 0:
                return []
        if row_max > 0:
            return [(row_max, 0)]
        elif col_max > 0:
            return [(0, col_max)]
        return [(0,0)]

    def add_cell(self, pos, val=None):
        r"""
        Add a cell to the graph.
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.add_cell((0,2))
        sage: ga
        Grid Graph for [3, 2]: Graph on 7 vertices
        """
        self.add_vertex(pos)

    def remove_cell(self, pos):
        r"""
        Remove a cell from the graph.
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.remove_cell((0,1))
        sage: ga
        Grid Graph for [3, 2]: Graph on 5 vertices
        """
        self.delete_vertex(pos)

    def add_row(self):
        r"""
        Add a row to the graph.
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.add_row()
        sage: ga
        Grid Graph for [3, 2]: Graph on 8 vertices
        """
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.add_vertices([(row_max + 1, j) for j in range(col_max + 1)])

    def insert_row(self, index):
        r"""
        Add a row at index
        Here, all rows play the same part,
        so we merely call add_row
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.insert_row(1)
        sage: ga
        Grid Graph for [3, 2]: Graph on 8 vertices
        """
        self.add_row()

    def remove_row(self, index=None):
        r"""
        Remove a row from the graph
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.remove_row()
        sage: ga
        Grid Graph for [3, 2]: Graph on 4 vertices
        """
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.delete_vertices([(row_max, j) for j in range(col_max + 1)])

    def add_column(self):
        r"""
        Add a column to the graph.
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.add_column()
        sage: ga
        Grid Graph for [3, 2]: Graph on 9 vertices
        """
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.add_vertices([(i, col_max + 1) for i in range(row_max + 1)])

    def insert_column(self, index):
        r"""
        Add a column at index
        Here, all columns play the same part,
        so we merely call add_column
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.insert_column(1)
        sage: ga
        Grid Graph for [3, 2]: Graph on 9 vertices
        """
        self.add_column()

    def remove_column(self, index=None):
        r"""
        Remove a column from the graph
        TESTS:
        sage: from sage.graphs.generators.basic import GridGraph
        sage: from sage_widget_adapters import GraphGridViewAdapter
        sage: ga = GraphGridViewAdapter(GridGraph((3,2)))
        sage: ga.remove_column()
        sage: ga
        Grid Graph for [3, 2]: Graph on 3 vertices
        """
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.delete_vertices([(i, col_max) for i in range(row_max + 1)])

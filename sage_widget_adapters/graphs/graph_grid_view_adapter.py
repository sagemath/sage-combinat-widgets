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
        cells = {}
        for v in self.vertices:
            cells[v] = None
        return cells

    @classmethod
    def from_cells(cells={}):
        g = Graph()
        g.add_vertices(list(cells.keys()))
        return g

    def addable_cells(self):
        r"""
        No cell should be added in isolation
        except for linear graphs
        """
        if not g.num_verts():
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
        self.add_vertex(pos)

    def remove_cell(self, pos):
        self.delete_vertex(pos)

    def add_row(self):
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.add_vertices([(row_max + 1, j) for j in range(col_max + 1)])

    def insert_row(self, index):
        r"""
        All rows play the same part
        """
        self.add_row()

    def remove_row(self, index):
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.remove_vertices([(row_max, j) for j in range(col_max + 1)])

    def add_column(self):
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.add_vertices([(i, col_max + 1) for i in range(row_max + 1)])

    def insert_column(self, index):
        r"""
        All rows have the same role
        """
        self.add_column()

    def remove_column(self, index):
        row_max, col_max = 0, 0
        for t in self.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        self.remove_vertices([(i, col_max) for i in range(row_max + 1)])

# -*- coding: utf-8 -*-
r"""
Grid View Adapter for matrices

**Grid View matrix operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~MatrixGridViewAdapter.compute_cells` | Compute matrix cells as a dictionary { coordinate pair : label }
    :meth:`~MatrixGridViewAdapter.from_cells` | Create a new matrix from a cells dictionary
    :meth:`~MatrixGridViewAdapter.get_cell` | Get the matrix cell value
    :meth:`~MatrixGridViewAdapter.set_cell` | Set the matrix cell value
    :meth:`~MatrixGridViewAdapter.addable_cells` | List addable cells
    :meth:`~MatrixGridViewAdapter.removable_cells` | List removable cells
    :meth:`~MatrixGridViewAdapter.add_cell` | Add a cell
    :meth:`~MatrixGridViewAdapter.remove_cell` | Remove a cell
    :meth:`~MatrixGridViewAdapter.append_row` | Append a row
    :meth:`~MatrixGridViewAdapter.insert_row` | Insert a row at given index
    :meth:`~MatrixGridViewAdapter.remove_row` | Remove a row at given index
    :meth:`~MatrixGridViewAdapter.append_column` | Append a column
    :meth:`~MatrixGridViewAdapter.insert_column` | Insert a column at given index
    :meth:`~MatrixGridViewAdapter.remove_column` | Remove a column at given index
"""

from sage.matrix.matrix2 import Matrix

class MatrixGridViewAdapter(Matrix):
    def __init__(self, parent):
        super(MatrixGridViewAdapter, self).__init__(parent)

    def compute_cells(self):
        cells = {}
        for i in self.numrows():
            r = self[i]
            for j in self.numcols():
                cells[(i,j)] = r[j]
        return cells

    @classmethod
    def from_cells(cells={}):
        rows = []
        i = 0
        while i < max(pos[0] for pos in cells):
            row = (cells[pos] for pos in cells if pos[0] == i)
            rows.append(row)
            i += 1
        return matrix(rows)

    def get_cell(self, pos):
        r"""
        Get cell content
        """
        if pos[0] >= self.nrows() or pos[1] >= self.ncols():
            raise ValueError("Entry '%s' does not exist!" % pos)
        return self[pos[0]][pos[1]]

    def set_cell(self, pos, val):
        r"""
        Edit matrix cell
        TESTS::
        sage: from sage_widget_adapters import MatrixGridViewAdapter
        sage: A = MatrixGridViewAdapter((QQ, 3, 3, range(9))/2)
        sage: A.edit_cell((0,1), 2/3)
        sage: A
        sage: A.edit_cell((2,2), pi)
        ---------------------------------------------------------------------------
        TypeError
        """
        if not val in self.base_ring():
            raise TypeError("Value '%s' is not compatible!" % val)
        B = matrix(self.base_ring(), 1, 1, val)
        self.set_block(pos[0], pos[1], val)

    def addable_cells(self):
        r"""
        No cell should be added in isolation
        except for vectors
        """
        if self.nrows() == 1:
            return [(0, self.ncols())]
        if self.ncols() == 1:
            return [(self.nrows(), 0)]
        return []

    def removable_cells(self):
        r"""
        No cell should be removed in isolation
        except for vectors
        """
        if self.nrows() == 1:
            return [(0, self.ncols()-1)]
        if self.ncols() == 1:
            return [(self.nrows()-1, 0)]
        return []

    def add_cell(self, pos, val):
        r"""
        No cell should be added in isolation
        except for vectors
        """
        if not pos in self.addable_cells():
            raise ValueError("Position '%s' is not addable." % str(pos))
        if pos[0] == 0:
            return self.augment(vector([val]))
        if pos[1] == 0:
            return self.stack(vector([val]))

    def remove_cell(self, pos):
        r"""
        No cell should be removed in isolation
        except for vectors
        """
        if not pos in self.removable_cells():
            return self
        if pos[0] == 0:
            return self.matrix_from_columns(range(self.ncols()-1))
        if pos[1] == 1:
            return self.matrix_from_rows(range(self.nrows()-1))

    def append_row(self, r=None):
        r"""
        """
        if not r:
            return self.stack(vector([0] * self.ncols()))
        for x in r:
            if not x in self.base_ring():
                raise TypeError("Value '%s' is not compatible!" % x)
        if len(r) > self.ncols():
            r = c[self.ncols()]
        elif len(r) < self.ncols():
            r = r + [0] * (self.ncols() - len(r))
        return self.stack(vector(r))

    def insert_row(self, index, r=None):
        r"""
        """
        if not r:
            r = [0] * self.ncols()
        else:
            for x in r:
                if not x in self.base_ring():
                    raise TypeError("Value '%s' is not compatible!" % x)
            if len(r) > self.ncols():
                r = c[self.ncols()]
            elif len(r) < self.ncols():
                r = r + [0] * (self.ncols() - len(r))
        top = self.matrix_from_rows(range(index))
        bottom = self.matrix_from_rows(range(index,self.nrows()))
        return top.stack(vector(r)).stack(bottom)

    def remove_row(self, index=None):
        r"""
        TESTS::
        sage: from sage.matrix.matrix_space import MatrixSpace
        sage: S = MatrixSpace(ZZ, 4,3)
        sage: from sage_widget_adapters import MatrixGridViewAdapter
        sage: A = MatrixGridViewAdapter(S,range(12))
        sage: A.remove_row(2)
        [ 0  1  2]
        [ 3  4  5]
        [ 9 10 11]
        sage: A.remove_row()
        [ 0  1  2]
        [ 3  4  5]
        [ 6  7  8]
        """
        if index is None:
            index = self.nrows() - 1
        return self.delete_rows([index])

    def append_column(self, c = None):
        r"""
        """
        if not c:
            self.augment(vector([0]*self.nrows()))
        for x in c:
            if not x in self.base_ring():
                raise TypeError("Value '%s' is not compatible!" % x)
        if len(c) > self.nrows():
            c = c[self.nrows()]
        elif len(c) < self.nrows():
            c = c + [0] * (self.nrows() - len(c))
        return self.augment(vector(c))

    def insert_column(self, index, c=None):
        r"""
        """
        if not c:
            c = [0] * self.nrows()
        else:
            for x in c:
                if not x in self.base_ring():
                    raise TypeError("Value '%s' is not compatible!" % x)
            if len(c) > self.nrows():
                c = c[self.nrows()]
            elif len(c) < self.nrows():
                c = c + [0] * (self.nrows() - len(c))
        left = self.matrix_from_columns(range(index))
        right = self.matrix_from_columns(range(index,self.nrows()))
        return left.stack(vector(c)).stack(right)

    def remove_column(self, index):
        r"""
        TESTS::
        sage: from sage_widget_adapters import MatrixGridViewAdapter
        sage: m = MatrixGridViewAdapter([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])
        sage: m.remove_column(1)
        [ 0  2]
        [ 3  5]
        [ 6  8]
        [ 9 11]
        sage: A.remove_column()
        [ 0  1]
        [ 3  4]
        [ 6  4]
        [ 9 10]
        """
        if index is None:
            index = self.ncols() - 1
        return self.delete_columns([index])

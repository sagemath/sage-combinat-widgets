# -*- coding: utf-8 -*-
r"""
Grid View Adapter for matrices

**Grid View matrix operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~TableauGridViewAdapter.cell_to_unicode` | Static method for typecasting cell content to unicode
    :meth:`~TableauGridViewAdapter.unicode_to_cell` | Static method for typecasting unicode to cell content
    :meth:`~MatrixGridViewAdapter.compute_cells` | Compute matrix cells as a dictionary { coordinate pair : label }
    :meth:`~MatrixGridViewAdapter.from_cells` | Create a new matrix from a cells dictionary
    :meth:`~MatrixGridViewAdapter.get_cell` | Get the matrix cell value
    :meth:`~MatrixGridViewAdapter.set_cell` | Set the matrix cell value
    :meth:`~MatrixGridViewAdapter.addable_cells` | List addable cells
    :meth:`~MatrixGridViewAdapter.removable_cells` | List removable cells
    :meth:`~MatrixGridViewAdapter.append_row` | Append a row
    :meth:`~MatrixGridViewAdapter.insert_row` | Insert a row at given index
    :meth:`~MatrixGridViewAdapter.remove_row` | Remove a row at given index
    :meth:`~MatrixGridViewAdapter.append_column` | Append a column
    :meth:`~MatrixGridViewAdapter.insert_column` | Insert a column at given index
    :meth:`~MatrixGridViewAdapter.remove_column` | Remove a column at given index

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
from sage.matrix.matrix2 import Matrix
from sage.matrix.constructor import matrix
from itertools import product
from sage.sets.finite_enumerated_set import FiniteEnumeratedSet
from sage.modules.free_module_element import vector
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter

class MatrixGridViewAdapter(GridViewAdapter):
    objclass = Matrix

    def __init__(self, obj):
        r"""
        Init an adapter object, set attributes `celltype` and `traitclass` (where applicable)
        TESTS::
            sage: from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
            sage: from sage.matrix.constructor import Matrix
            sage: m = Matrix(QQ, 3, 3, range(9))/2
            sage: ma = MatrixGridViewAdapter(m)
        """
        super(MatrixGridViewAdapter, self).__init__()
        self.ring = obj.base_ring()
        try:
            self.celltype = self.ring.element_class
        except:
            try:
                if hasattr(self.ring, 'an_element'):
                    self.celltype = self.ring.an_element().__class__
                elif hasattr(self.ring, 'random_element'):
                    self.celltype = self.ring.random_element().__class__
                else:
                    raise TypeError("Cannot determine matrix base ring elements class.")
            except:
                raise TypeError("Cannot determine matrix base ring elements class.")
        self.cellzero = self.ring.zero()

    def unicode_to_cell(self, s):
        r"""
        From an unicode string `s`,
        return matching cell value.
        """
        if s:
            try:
                return self.ring(s)
            except:
                try:
                    return self.celltype(s)
                except:
                    raise ValueError("Cannot cast unicode %s to object %s cell" % (s, self.value))
        return self.cellzero

    @staticmethod
    def compute_cells(obj):
        r"""
        From a matrix `obj`,
        return a dictionary { coordinates pair : cell value (as a Sage object) }
        """
        return {(i,j):obj[i][j] for (i,j) in product(range(obj.nrows()), range(len(obj[0])))}

    @classmethod
    def from_cells(cls, cells={}):
        nrows, ncols = 0, 0
        width = 0
        for pos in cells:
            nrows = max(nrows, pos[0]+1)
            ncols = max(ncols, pos[1]+1)
        rows = [[cells[(i,j)] for j in range(ncols)] for i in range(nrows)]
        return matrix(rows)

    @staticmethod
    def get_cell(obj, pos):
        r"""
        Get cell content
        """
        if pos[0] >= obj.nrows() or pos[1] >= obj.ncols():
            raise ValueError("Entry '%s' does not exist!" % pos)
        return obj[pos[0]][pos[1]]

    @classmethod
    def set_cell(cls, obj, pos, val):
        r"""
        Edit matrix cell
        TESTS::
        sage: from sage.matrix.constructor import Matrix
        sage: from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        sage: A = Matrix(QQ, 3, 3, range(9))/2
        sage: MatrixGridViewAdapter.set_cell(A, (0,1), 2/3)
        [  0 2/3   1]
        [3/2   2 5/2]
        [  3 7/2   4]
        sage: MatrixGridViewAdapter.set_cell(A, (2,2), pi)
        Traceback (most recent call last):
        ...
        TypeError: Value 'pi' is not compatible!
        """
        if not val in obj.base_ring():
            raise TypeError("Value '%s' is not compatible!" % val)
        B = matrix(obj.base_ring(), 1, 1, val)
        obj.set_block(pos[0], pos[1], B)
        return obj

    @staticmethod
    def addable_cells(obj):
        r"""
        No cell should be added in isolation
        except for vectors
        """
        if obj.nrows() == 1:
            return [(0, obj.ncols())]
        if obj.ncols() == 1:
            return [(obj.nrows(), 0)]
        return []

    @staticmethod
    def removable_cells(obj):
        r"""
        No cell should be removed in isolation
        except for vectors
        """
        if obj.nrows() == 1:
            return [(0, obj.ncols()-1)]
        if obj.ncols() == 1:
            return [(obj.nrows()-1, 0)]
        return []

    def append_row(self, obj, r=None):
        r"""
        """
        if not r:
            return obj.stack(vector([self.cellzero] * obj.ncols()))
        if len(r) > obj.ncols():
            print("Row is too long. Truncating")
            r = r[:obj.ncols()]
        elif len(r) < obj.ncols():
            r = list(r) + [self.cellzero] * (obj.ncols() - len(r))
        return obj.stack(vector([self.unicode_to_cell(x) for x in r]))

    def insert_row(self, obj, index, r=None):
        r"""
        TESTS::
        sage: from sage.matrix.matrix_space import MatrixSpace
        sage: S = MatrixSpace(ZZ, 4,3)
        sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
        sage: from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        sage: ma = MatrixGridViewAdapter(m)
        sage: ma.insert_row(m, 1, (1,2,3))
        [ 1  7  1]
        [ 1  2  3]
        [ 0  0  3]
        [ 0 -1  2]
        [ 1  0 -3]
        """
        if not r:
            r = [self.cellzero] * obj.ncols()
        else:
            if len(r) > obj.ncols():
                print("Row is too long. Truncating")
                r = r[:obj.ncols()]
            elif len(r) < obj.ncols():
                r = list(r) + [self.cellzero] * (obj.ncols() - len(r))
        top = obj.matrix_from_rows(range(index))
        bottom = obj.matrix_from_rows(range(index,obj.nrows()))
        return top.stack(vector([self.unicode_to_cell(x) for x in r])).stack(bottom)

    @classmethod
    def remove_row(cls, obj, index=None):
        r"""
        TESTS::
        sage: from sage.matrix.matrix_space import MatrixSpace
        sage: S = MatrixSpace(ZZ, 4,3)
        sage: from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        sage: A = S.matrix([0,1,2,3,4,5,6,7,8,9,10,11])
        sage: MatrixGridViewAdapter.remove_row(A, 2)
        [ 0  1  2]
        [ 3  4  5]
        [ 9 10 11]
        sage: MatrixGridViewAdapter.remove_row(A)
        [0 1 2]
        [3 4 5]
        [6 7 8]
        """
        if index is None:
            index = obj.nrows() - 1
        return obj.delete_rows([index])

    def append_column(self, obj, c=None):
        r"""
        """
        if not c:
            return obj.augment(vector([self.cellzero]*obj.nrows()))
        if len(c) > obj.nrows():
            print("Column is too long. Truncating")
            c = c[:obj.nrows()]
        elif len(c) < obj.nrows():
            c = list(c) + [self.cellzero] * (obj.nrows() - len(c))
        return obj.augment(vector([self.unicode_to_cell(x) for x in c]))

    def insert_column(self, obj, index, c=None):
        r"""
        TESTS::
        sage: from sage.matrix.matrix_space import MatrixSpace
        sage: S = MatrixSpace(ZZ, 4,3)
        sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
        sage: from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        sage: ma = MatrixGridViewAdapter(m)
        sage: ma.insert_column(m, 1, (1,1,1))
        [ 1  1  7  1]
        [ 0  1  0  3]
        [ 0  1 -1  2]
        [ 1  0  0 -3]
        sage: ma.insert_column(m, 2, (1,1,1,2,2,2))
        Column is too long. Truncating
        [ 1  7  1  1]
        [ 0  0  1  3]
        [ 0 -1  1  2]
        [ 1  0  2 -3]
        """
        if not c:
            c = [self.cellzero] * obj.nrows()
        else:
            if len(c) > obj.nrows():
                print("Column is too long. Truncating")
                c = c[:obj.nrows()]
            elif len(c) < obj.nrows():
                c = list(c) + [self.cellzero] * (obj.nrows() - len(c))
        left = obj.matrix_from_columns(range(index))
        right = obj.matrix_from_columns(range(index,obj.ncols()))
        return left.augment(vector([self.unicode_to_cell(x) for x in c])).augment(right)

    @classmethod
    def remove_column(cls, obj, index=None):
        r"""
        TESTS::
        sage: from sage.matrix.matrix_space import MatrixSpace
        sage: S = MatrixSpace(ZZ, 4,3)
        sage: from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        sage: A = S.matrix([0,1,2,3,4,5,6,7,8,9,10,11])
        sage: MatrixGridViewAdapter.remove_column(A, 1)
        [ 0  2]
        [ 3  5]
        [ 6  8]
        [ 9 11]
        sage: MatrixGridViewAdapter.remove_column(A)
        [ 0  1]
        [ 3  4]
        [ 6  7]
        [ 9 10]
        """
        if index is None:
            index = obj.ncols() - 1
        return obj.delete_columns([index])

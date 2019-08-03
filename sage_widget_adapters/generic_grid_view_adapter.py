# -*- coding: utf-8 -*-
r"""
Generic Grid View Adapter

**Grid View operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GridViewAdapter.cell_to_display` | Static method for typecasting cell content to widget display value
    :meth:`~GridViewAdapter.display_to_cell` | Instance method for typecasting widget display value to cell content
    :meth:`~GridViewAdapter.compute_cells` | Compute object cells as a dictionary { coordinate pair : integer }
    :meth:`~GridViewAdapter.from_cells` | Create a new Sage object from a cells dictionary
    :meth:`~GridViewAdapter._validate` | Validate a new object
    :meth:`~GridViewAdapter.get_cell` | Get the object cell content
    :meth:`~GridViewAdapter.set_cell` | Set the object cell content
    :meth:`~GridViewAdapter.addable_cells` | List addable cells
    :meth:`~GridViewAdapter.removable_cells` | List removable cells
    :meth:`~GridViewAdapter.add_cell` | Add a cell at given position
    :meth:`~GridViewAdapter.remove_cell` | Remove a cell from given position
    :meth:`~GridViewAdapter.append_row` | Append a row
    :meth:`~GridViewAdapter.insert_row` | Insert a row at given index
    :meth:`~GridViewAdapter.remove_row` | Remove a row at given index
    :meth:`~GridViewAdapter.append_column` | Append a column
    :meth:`~GridViewAdapter.insert_column` | Insert a column at given index
    :meth:`~GridViewAdapter.remove_column` | Remove a column at given index

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
import traitlets, sage.all
from sage.all import SageObject
from sage.misc.abstract_method import abstract_method
from six import text_type

import __main__
def eval_in_main(s):
    """
    Evaluate the expression `s` in the global scope

    TESTS ::

        sage: from sage_widget_adapters.generic_grid_view_adapter import eval_in_main
        sage: from sage.combinat.tableau import Tableaux
        sage: eval_in_main("Tableaux")
        <class 'sage.combinat.tableau.Tableaux'>
    """
    try:
        return eval(s, sage.all.__dict__)
    except:
        return eval(s, __main__.__dict__)

class GridViewAdapter(object):
    r"""
    A generic grid view adapter.

    ATTRIBUTES::

        * ``objclass`` -- object class for this adapter
        * ``constructorname`` -- name of the constructor that builds a math object from a list
        * ``traitclass`` -- cells trait class
        * ``celltype`` -- cell content object type (to be defined in subclasses)
        * ``cellzero`` -- cell content zero (to be defined in subclasses)
        * ``addablecelltype`` -- addable cell content zero (to be defined in subclasses) -- by default = celltype
        * ``addablecellzero`` -- addable cell content zero (to be defined in subclasses) -- by default == cellzero
    """
    objclass = SageObject
    constructorname = None
    traitclass = traitlets.Instance
    constructorname = None
    addablecelltype = None
    addablecellzero = None

    @staticmethod
    def cell_to_display(cell_content, display_type=text_type):
        r"""
        From a cell value `cell_content`,
        return widget display value.

        TESTS ::

            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: from six import text_type
            sage: GridViewAdapter.cell_to_display(1, text_type)
            '1'
            sage: GridViewAdapter.cell_to_display(True, bool)
            True
        """
        if display_type == text_type:
            return str(cell_content)
        return cell_content

    def display_to_cell(self, display_value, display_type=text_type):
        r"""
        From an unicode string `s`,
        return matching cell value.

        TESTS ::

            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: from six import text_type
            sage: a.display_to_cell('1', text_type)
            Traceback (most recent call last):
            ...
            AttributeError: 'GridViewAdapter' object has no attribute 'celltype'
        """
        if display_value:
            return self.celltype(display_value)
        return self.cellzero

    @staticmethod
    @abstract_method
    def compute_cells(obj):
        r"""
        From an object `obj`,
        return a dictionary { coordinates pair : integer }
        """

    @classmethod
    def _validate(cls, obj, constructorname=''):
        r"""
        From an object `obj`,
        Try to build an object of type `cls`.

        TESTS ::

            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: assert issubclass(GridViewAdapter._validate(pi).__class__, SageObject)
            sage: from sage.matrix.constructor import matrix
            sage: assert issubclass(GridViewAdapter._validate(pi, constructorname='matrix').__class__, BaseException)
        """
        try:
            if constructorname:
                return eval_in_main(constructorname)(obj)
            if cls.constructorname:
                return eval_in_main(cls.constructorname)(obj)
            if issubclass(obj.__class__, cls.objclass):
                return obj
            return cls.objclass(obj)
        except Exception as e:
            return e

    @classmethod
    @abstract_method
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : integer },
        return a Sage object.
        """

    @staticmethod
    def get_cell(obj, pos):
        r"""
        From an object and a tuple `pos`,
        return the object cell value at position `pos`.

        TESTS ::

            sage: from sage.matrix.constructor import Matrix
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: m = Matrix(QQ, 3, 3, range(9))/2
            sage: GridViewAdapter.get_cell(m, (1,2))
            5/2
            sage: from sage.combinat.tableau import Tableau
            sage: t = Tableau([[1, 2, 5, 6], [3, 7], [4]])
            sage: GridViewAdapter.get_cell(t, (1,1))
            7
            sage: GridViewAdapter.get_cell(t, (1,6))
            Traceback (most recent call last):
            ...
            ValueError: Cell '(1, 6)' does not exist!
            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: st = SkewTableau([[None,1,2],[3,4,5],[6]])
            sage: GridViewAdapter.get_cell(st, (0,0))
            sage: GridViewAdapter.get_cell(st, (1,1))
            4
        """
        try:
            return obj[pos[0]][pos[1]]
        except:
            pass
        try:
            l = [list(x) for x in obj]
        except:
            raise NotImplementedError("Adapter class method 'get_cell(obj, pos)' is not implemented.")
        try:
            return l[pos[0]][pos[1]]
        except:
            raise ValueError("Cell '%s' does not exist!" % str(pos))

    def make_dirty(self, l, dirty={}):
        r"""
        Append 'dirty' values to list 'l'.
        Return a list with no empty values.

        TESTS ::

            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: from sage.combinat.tableau import Tableau
            sage: t = Tableau([[1, 2, 5, 6], [3, 7], [4]])
            sage: ga = GridViewAdapter()
            sage: ga.cellzero = 0
            sage: ga.make_dirty(t.to_list(), {(1,2):42})
            [[1, 2, 5, 6], [3, 7, 42], [4]]
            sage: ga.make_dirty(t.to_list(), {(2,0):0})
            [[1, 2, 5, 6], [3, 7]]
        """
        for p in dirty:
            if p[0] < len(l):
                if p[1] < len(l[p[0]]):
                    if dirty[p] == self.cellzero:
                        del l[p[0]][p[1]]
                    else:
                        l[p[0]][p[1]] = dirty[p]
                elif len(l[p[0]]) == p[1] and dirty[p] != self.cellzero:
                    l[p[0]].append(dirty[p])
            else:
                for i in range(p[0] - len(l)):
                    l.append([])
                l.append([dirty[p]])
        return [val for val in l if val]

    def set_cell(self, obj, pos, val, dirty={}, constructorname=''):
        r"""
        From a Sage object, a position (pair of coordinates) `pos` and a value `val`,
        return a new Sage object.
        with a modified cell at position `pos`.

        TESTS ::

            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: from sage.combinat.tableau import Tableau
            sage: t = Tableau([[1, 2, 5, 6], [3, 7], [4]])
            sage: ga = GridViewAdapter()
            sage: ga.set_cell(t, (1,1), 8, constructorname='Tableau')
            [[1, 2, 5, 6], [3, 8], [4]]
            sage: ga.cellzero = 0
            sage: ga.set_cell(t, (0,3), 6, {(0,3):5}, constructorname='StandardTableau')
            [[1, 2, 5, 6], [3, 7], [4]]
            sage: from sage.matrix.constructor import Matrix, matrix
            sage: m = Matrix(QQ, 3, 3, range(9))/2
            sage: ga.set_cell(m, (0,1), 2/3, constructorname='matrix')
            [  0 2/3   1]
            [3/2   2 5/2]
            [  3 7/2   4]
            sage: ga.set_cell(m, (4,2), 1/2, constructorname='matrix')
            Traceback (most recent call last):
            ...
            ValueError: Position '(4, 2)' does not exist
        """
        try:
            l = [list(x) for x in obj]
        except:
            raise NotImplementedError("Adapter method 'set_cell(obj, pos, val)' is not implemented.")
        l = self.make_dirty(l, dirty)
        try:
            l[pos[0]][pos[1]] = val
        except:
            raise ValueError("Position '%s' does not exist" % str(pos))
        return self._validate(l, constructorname)

    @staticmethod
    @abstract_method(optional = True)
    def addable_cells(obj):
        r"""
        For Sage object `obj`,
        list those cell positions where a user could want to add a cell,
        and get a still valid Sage object for this adapter.
        """

    @staticmethod
    @abstract_method(optional = True)
    def removable_cells(obj):
        r"""
        For Sage object `obj`,
        list those cell positions where a user could want to remove a cell,
        and get a still valid Sage object for this adapter.
        """

    @abstract_method(optional = True)
    def add_cell(self, obj, pos, val, dirty={}):
        r"""
        This method should try to add a cell to object `obj`
        at position `pos` and with value `val`.
        """

    @abstract_method(optional = True)
    def remove_cell(self, obj, pos, dirty={}):
        r"""
        This method should try to remove a cell from object `obj`
        at position `pos`.
        """

    @abstract_method(optional = True)
    def append_row(self, obj, r=None):
        r"""
        This method should try to append a row to object `obj`
        with values from list `r`.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.append_row(S, (1,2,3)) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: 'AbstractMethod' object is not callable
        """

    @abstract_method(optional = True)
    def insert_row(self, obj, index, r=None):
        r"""
        This method should try to insert a row to object `obj`
        at index `index`, with values from list `r`.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.insert_row(S, 1, (1,2,3)) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: 'AbstractMethod' object is not callable
        """

    def add_row(self, obj, index=None, r=None):
        r"""
        An alias for appending/inserting a row.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.add_row(S, 1, (1,2,3,4))
            Traceback (most recent call last):
            ...
            NotImplementedError: Method 'insert_row' is not implemented.
        """
        if index:
            try:
                return self.insert_row(obj, index, r)
            except:
                raise NotImplementedError("Method 'insert_row' is not implemented.")
        else:
            try:
                return self.append_row(obj, r)
            except:
                raise NotImplementedError("Method 'append_row' is not implemented.")

    @abstract_method(optional = True)
    def remove_row(self, obj, index=None):
        r"""
        This method should try to remove a row from object `obj`
        at index `index`.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.remove_row(S, 1) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: 'AbstractMethod' object is not callable
        """

    @abstract_method(optional = True)
    def append_column(self, obj, r=None):
        r"""
        This method should try to append a column to object `obj`
        with values from list `r`.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.append_column(S, (1,2,3,4)) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: 'AbstractMethod' object is not callable
        """

    @abstract_method(optional = True)
    def insert_column(self, obj, index, r=None):
        r"""
        This method should try to insert a column to object `obj`
        at index `index`, with values from list `r`.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.insert_column(S, 1, (1,2,3,4)) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: 'AbstractMethod' object is not callable
        """

    @abstract_method(optional = True)
    def remove_column(self, obj, index=None):
        r"""
        This method should try to remove a column from object `obj`
        at index `index`.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.remove_column(S, 2) #doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: 'AbstractMethod' object is not callable
        """

    def add_column(self, obj, index=None, r=None):
        r"""
        An alias for appending/inserting a column.

        TESTS ::

            sage: from sage.matrix.matrix_space import MatrixSpace
            sage: S = MatrixSpace(ZZ, 4,3)
            sage: m = S.matrix([1,7,1,0,0,3,0,-1,2,1,0,-3])
            sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
            sage: a = GridViewAdapter()
            sage: a.add_column(S, 1, (1,2,3))
            Traceback (most recent call last):
            ...
            NotImplementedError: Method 'insert_column' is not implemented.
        """
        if index:
            try:
                return self.insert_column(obj, index, r)
            except:
                raise NotImplementedError("Method 'insert_column' is not implemented.")
        else:
            try:
                return self.append_column(obj, r)
            except:
                raise NotImplementedError("Method 'append_column' is not implemented.")

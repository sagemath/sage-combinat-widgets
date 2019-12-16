# -*- coding: utf-8 -*-
r"""
Grid View Adapter for skew tableaux

**Grid View skew tableau operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~SkewTableauGridViewAdapter.compute_cells` | Compute skew tableau cells as a dictionary { coordinate pair : Integer }
    :meth:`~SkewTableauGridViewAdapter.from_cells` | Create a new skew tableau from a cells dictionary
    :meth:`~SkewTableauGridViewAdapter.addable_cells` | List addable cells
    :meth:`~SkewTableauGridViewAdapter.removable_cells` | List removable cells
    :meth:`~SkewTableauGridViewAdapter.add_cell` | Add a cell
    :meth:`~SkewTableauGridViewAdapter.remove_cell` | Remove a cell

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from sage.combinat.skew_tableau import SkewTableau
from sage.rings.integer import Integer
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter


class SkewTableauGridViewAdapter(GridViewAdapter):
    r"""
    Grid view adapter for skew tableaux.

    ATTRIBUTES::
        * ``objclass`` -- SkewTableau
        * ``celltype`` -- Integer
        * ``cellzero`` -- Integer(0)
    """
    objclass = SkewTableau
    constructorname = 'SkewTableau'
    celltype = Integer # i.e. sage.rings.integer.Integer
    cellzero = Integer(0)

    @staticmethod
    def compute_cells(obj):
        r"""
        From a skew tableau,
        return a dictionary { coordinates pair : Integer }
        TESTS ::

            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: from sage_widget_adapters.combinat.skew_tableau_grid_view_adapter import SkewTableauGridViewAdapter
            sage: st = SkewTableau([[None, None, 1, 2], [None, 1], [4]])
            sage: SkewTableauGridViewAdapter.compute_cells(st)
            {(0, 2): 1, (0, 3): 2, (1, 1): 1, (2, 0): 4}
        """
        return {(i,j):obj[i][j] for (i,j) in obj.cells()}

    @classmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : Integer }
        return a corresponding skew tableau
        TESTS ::

            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: from sage_widget_adapters.combinat.skew_tableau_grid_view_adapter import SkewTableauGridViewAdapter
            sage: SkewTableauGridViewAdapter.from_cells({(0, 1): 2, (1, 0): 3, (2, 0): 4})
            [[None, 2], [3], [4]]
        """
        rows = []
        for i in range(max(pos[0] for pos in cells) + 1):
            rows.append([None] * (max(pos[1] for pos in cells if pos[0] == i) + 1))
        for pos in cells:
            rows[pos[0]][pos[1]] = cells[pos]
        try:
            return cls.objclass(rows)
        except:
            raise TypeError(
                "This object is not compatible with this adapter (%s, for %s objects)" % (cls, cls.objclass))

    @staticmethod
    def addable_cells(obj):
        r"""
        List object addable cells
        TESTS ::

            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: from sage_widget_adapters.combinat.skew_tableau_grid_view_adapter import SkewTableauGridViewAdapter
            sage: st = SkewTableau([[None, None, None, 1], [None, None, 2], [None, 1], [4]])
            sage: SkewTableauGridViewAdapter.addable_cells(st)
            [(0, 2), (1, 1), (2, 0), (0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]
        """
        return obj.shape().inner().corners() + obj.shape().outer().outside_corners()

    @staticmethod
    def removable_cells(obj):
        r"""
        List object removable cells
        TESTS ::

            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: from sage_widget_adapters.combinat.skew_tableau_grid_view_adapter import SkewTableauGridViewAdapter
            sage: st = SkewTableau([[None, None, None, 1, 2, 6], [None, None, 3, 4], [None, 1], [5]])
            sage: SkewTableauGridViewAdapter.removable_cells(st)
            [(0, 5), (1, 3), (2, 1), (3, 0), (0, 3), (1, 2)]
        """
        ret = obj.shape().outer().corners()
        for c in obj.shape().inner().outside_corners():
            if not c in ret:
                ret.append(c)
        return ret

    def add_cell(self, obj, pos, val, dirty={}):
        r"""
        Add cell.

        TESTS ::

            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: from sage_widget_adapters.combinat.skew_tableau_grid_view_adapter import SkewTableauGridViewAdapter
            sage: st = SkewTableau([[None, None, None, 2], [None, 1, 1], [1], [4]])
            sage: sta = SkewTableauGridViewAdapter()
            sage: sta.add_cell(st, (0, 2), 1)
            [[None, None, 1, 2], [None, 1, 1], [1], [4]]
            sage: sta.add_cell(st, (4, 0), 7)
            [[None, None, None, 2], [None, 1, 1], [1], [4], [7]]
            sage: sta.add_cell(st, (1, 1), 9)
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 1)' is not addable.
        """
        if not pos in self.addable_cells(obj):
            raise ValueError("Cell position '%s' is not addable." % str(pos))
        sl = obj.to_list()
        sl = self.make_dirty(sl, dirty)
        if pos[0] >= len(obj):
            sl.append([val])
        elif pos in obj.shape().outer().outside_corners():
            sl[pos[0]].append(val)
        else:
            sl[pos[0]][pos[1]] = val
        return self._validate(sl)

    def remove_cell(self, obj, pos, dirty={}):
        r"""
        Remove cell.

        TESTS ::

            sage: from sage.combinat.skew_tableau import SkewTableau
            sage: from sage_widget_adapters.combinat.skew_tableau_grid_view_adapter import SkewTableauGridViewAdapter
            sage: st = SkewTableau([[None, None, None, 1, 2, 6], [None, None, 3, 4], [None, 1], [5]])
            sage: sta = SkewTableauGridViewAdapter()
            sage: sta.remove_cell(st, (0, 0))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(0, 0)' is not removable.
            sage: sta.remove_cell(st, (0, 3))
            [[None, None, None, None, 2, 6], [None, None, 3, 4], [None, 1], [5]]
            sage: sta.remove_cell(st, (2, 1))
            [[None, None, None, 1, 2, 6], [None, None, 3, 4], [None], [5]]
            sage: st = SkewTableau([[None, None, 1, 2, 3], [None, 1], [4]])
            sage: sta.remove_cell(st, (0, 4))
            [[None, None, 1, 2], [None, 1], [4]]
        """
        if not pos in self.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))
        sl = obj.to_list()
        sl = self.make_dirty(sl, dirty)
        if len(sl[pos[0]]) == 1:
            del(sl[pos[0]])
        elif pos in obj.shape().outer().corners():
            sl[pos[0]].pop()
        else:
            sl[pos[0]][pos[1]] = None
        return self._validate(sl)

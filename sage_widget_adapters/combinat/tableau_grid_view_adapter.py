# -*- coding: utf-8 -*-
r"""
Grid View Adapter for tableaux

**Grid View tableau operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~TableauGridViewAdapter.compute_cells` | Compute tableau cells as a dictionary { coordinate pair : label }
    :meth:`~TableauGridViewAdapter.from_cells` | Create a new tableau from a cells dictionary
    :meth:`~TableauGridViewAdapter.get_cell` | Get the tableau cell content
    :meth:`~TableauGridViewAdapter.set_cell` | Set the tableau cell content
    :meth:`~TableauGridViewAdapter.addable_cells` | List addable cells
    :meth:`~TableauGridViewAdapter.removable_cells` | List removable cells
    :meth:`~TableauGridViewAdapter.add_cell` | Add a cell
    :meth:`~TableauGridViewAdapter.remove_cell` | Remove a cell
"""

from sage.combinat.tableau import *
from traitlets import Integer

class TableauGridViewAdapter(Tableau):
    traitclass = Integer

    @staticmethod
    def cell_to_unicode(cell_content):
        return str(cell_content)

    @staticmethod
    def unicode_to_cell(s):
        return int(s)

    def compute_cells(self):
        r"""
        From a tableau,
        return a dictionary { coordinates pair : integer }
        TESTS:
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.compute_cells()
        {(0, 0): 1, (0, 1): 2, (0, 2): 5, (0, 3): 6, (1, 0): 3, (2, 0): 4}
        """
        cells = {}
        for i in range(len(self)):
            r = self[i]
            for j in range(len(r)):
                cells[(i,j)] = r[j]
        return cells

    @classmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : integer }
        return a corresponding tableau
        TESTS:
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: TableauGridViewAdapter.from_cells({(0, 0): 1, (0, 1): 2, (0, 2): 5, (0, 3): 6, (1, 0): 3, (2, 0): 4})
        [[1, 2, 5, 6], [3], [4]]
        """
        rows = []
        i = 0
        while i <= max(pos[0] for pos in cells):
            row = [cells[pos] for pos in cells if pos[0] == i]
            row.sort()
            rows.append(row)
            i += 1
        return cls.__classcall_private__(cls, rows)

    def get_cell(self, pos):
        r"""
        Get cell value
        TESTS::
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.get_cell((1,1))
        7
        """
        try:
            return self.__call__(pos)
        except:
            raise ValueError("Cell %s does not exist!" % str(pos))

    def set_cell(self, pos, val):
        r"""
        Set cell value
        TESTS::
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.set_cell((1,1), 8)
        sage: gt.get_cell((1,1))
        8
        """
        tl = self.to_list()
        nl = []
        for i in range(len(tl)):
            l = tl[i]
            if i == pos[0]:
                l[pos[1]] = val
            nl.append(l)
        try:
            new_obj = self.__init__(self.parent(), tl)
        except:
            raise ValueError("Value '%s' is not compatible!" % val)
        else:
            return new_obj

    def addable_cells(self):
        r"""
        List addable cells
        TESTS::
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.addable_cells()
        [(0, 4), (1, 2), (2, 1), (3, 0)]
        """
        return self.shape().outside_corners()

    def removable_cells(self):
        r"""
        List removable cells
        TESTS::
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.removable_cells()
        [(0, 3), (1, 1), (2, 0)]
        """
        return self.corners()

    def add_cell(self, pos, val):
        r"""
        Add cell
        TESTS::
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.add_cell((3, 0), 8)
        sage: gt.add_cell((2, 0), 9) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: Cell position '(2, 0)' is not addable.
        """
        if not pos in self.addable_cells():
            raise ValueError("Position '%s' is not addable." % str(pos))
        tl = self.to_list()
        if pos[0] >= len(tl):
            nl = tl + [val]
        else:
            nl = []
            for i in range(len(tl)):
                l = tl[i]
                if i == pos[0]:
                    l.append(val)
                nl.append(l)
        try:
            new_obj = self.__init__(self.parent(), tl)
        except:
            raise ValueError("Cannot create a %s with this list!" % self.parent())
        else:
            return new_obj

    def remove_cell(self, pos):
        r"""
        Remove cell
        TESTS::
        sage: from sage.combinat.tableau import StandardTableau
        sage: from sage_widget_adapters import TableauGridViewAdapter
        sage: t = StandardTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: gt = TableauGridViewAdapter(t.parent(), t)
        sage: gt.remove_cell((1, 1))
        sage: gt.remove_cell((2, 1)) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: Cell position '(2, 1)' is not removable.
        """
        if not pos in self.removable_cells():
            raise ValueError("Position '%s' is not removable." % str(pos))
        tl = self.to_list()
        nl = []
        for i in range(len(tl)):
            l = tl[i]
            if i == pos[0]:
                l.pop()
            nl.append(l)
        try:
            new_obj = self.__init__(self.parent(), tl)
        except:
            raise ValueError("Cannot create a %s with this list!" % self.parent())
        else:
            return new_obj

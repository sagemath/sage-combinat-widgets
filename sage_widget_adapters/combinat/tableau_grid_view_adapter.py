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

from sage.combinat.tableau import Tableau

class TableauGridViewAdapter(Tableau):
    def compute_cells(self):
        cells = {}
        for i in len(self):
            r = self[i]
            for j in r:
                cells[(i,j)] = r[j]
        return cells

    @classmethod
    def from_cells(cells={}):
        rows = []
        i = 0
        while i < max(pos[0] for pos in cells):
            row = [cells[pos] for pos in cells if pos[0] == i]
            row.sort()
            rows.append(row)
            i += 1
        return tableau(rows)

    def get_cell(self, pos):
        try:
            return self.__call__(pos)
        except:
            raise ValueError("Cell %s does not exist!" % pos)

    def set_cell(self, pos, val):
        r"""
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
        return self.value.shape().outside_corners()

    def removable_cells(self):
        return self.value.corners()

    def add_cell(self, pos, val):
        if not pos in self.addable_cells():
            raise ValueError("Position '%s' is not addable!" % pos)
        tl = self.to_list()
        if i >= len(tl):
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
        if not pos in self.removable_cells():
            raise ValueError("Position '%s' is not removable!" % pos)
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

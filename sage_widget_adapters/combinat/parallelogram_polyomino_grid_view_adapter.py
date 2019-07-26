# -*- coding: utf-8 -*-
r"""
Grid View Adapter for parallelogram polyominos

**Grid View parallelogram polyominos operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~ParallelogramPolyominoGridViewAdapter.compute_cells` | Compute parallelogram polyomino celss as a dictionary { coordinate pair : False }
    :meth:`~ParallelogramPolyominoGridViewAdapter.addable_cells` | List addable cells
    :meth:`~ParallelogramPolyominoGridViewAdapter.removable_cells` | List removable cells
    :meth:`~ParallelogramPolyominoGridViewAdapter.add_cell` | Add a cell
    :meth:`~ParallelogramPolyominoGridViewAdapter.remove_cell` | Remove a cell

AUTHORS ::

    Henri Derycke

"""
from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter

class ParallelogramPolyominoGridViewAdapter(GridViewAdapter):
    r"""
    Grid view adapter for parallelogram polyominos.

    ATTRIBUTES::
        * ``objclass`` -- ParallelogramPolyomino
        * ``celltype`` -- bool
        * ``cellzero`` -- False
    """
    objclass = ParallelogramPolyomino
    celltype = bool
    cellzero = False

    @staticmethod
    def compute_cells(obj):
        r"""
        From a parallelogram polyomino,
        return a dictionary { coordinates pair : False }

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import ParallelogramPolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 1, 1],[1, 1 ,0]])
            sage: ParallelogramPolyominoGridViewAdapter.compute_cells(pp)
            {(0, 0): True, (0, 1): True}
        """
        cells = {}
        lower_heights = obj.lower_heights()
        upper_heights = obj.upper_heights()
        for i in range(obj.width()):
            for j in range(upper_heights[i],lower_heights[i]):
                cells[j,i] = True
        return cells

    @staticmethod
    def addable_cells(obj):
        r"""
        List object addable cells

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import ParallelogramPolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 1, 0, 1], [1, 1, 0, 0]])
            sage: ParallelogramPolyominoGridViewAdapter.addable_cells(pp)
            [(1, 0), (2, 1), (1, 2)]
        """
        cells = []

        upper_heights = obj.upper_heights()
        for i,c in enumerate(upper_heights[1:]):
            if c != upper_heights[i]:
                cells.append((c-1,i+1))

        lower_heights = obj.lower_heights()
        for i,c in enumerate(lower_heights[1:]):
            if c != lower_heights[i]:
                cells.append((lower_heights[i],i))

        height, width = obj.geometry()
        cells += [(height,width-1), (height-1,width)]

        return cells

    @staticmethod
    def removable_cells(obj):
        r"""
        List object removable cells

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import ParallelogramPolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 0, 1, 1], [1, 1, 0, 0]])
            sage: ParallelogramPolyominoGridViewAdapter.removable_cells(pp)
            [(1, 0), (0, 1)]
        """
        heights = [(0,0)] + list(zip(obj.upper_heights(),obj.lower_heights()))
        heights.append((heights[-1][1],)*2)
        cells = []
        for i in range(1,len(heights)-1):
            x1,y1 = heights[i-1]
            x2,y2 = heights[i]
            x3,y3 = heights[i+1]
            if x2+1 < y2 and x2 != x3 and x2+1 < y1:
                cells.append((x2,i-1))
            if x2 < y2-1 and y1 != y2 and y2-1 > x3:
                cells.append((y2-1,i-1))

        if len(heights) > 3:
            x1,y1 = heights[-3]
            x2,y2 = heights[-2]
            if y1 < y2 or x2+1 == y2:
                cells.append((y2-1, len(heights)-3))

        return cells

    def add_cell(self, obj, pos, val=None, dirty={}):
        r"""
        Add cell

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import ParallelogramPolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 1, 0, 1], [1, 1, 0, 0],])
            sage: ppa = ParallelogramPolyominoGridViewAdapter()
            sage: ppa.add_cell(pp, (1, 0))
            [[0, 0, 1, 1], [1, 1, 0, 0]]
            sage: ppa.add_cell(pp, (1, 1))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 1)' is not addable.
        """
        if pos not in self.addable_cells(obj):
            raise ValueError("Cell position '%s' is not addable." % str(pos))

        heights = list(zip(obj.upper_heights(),obj.lower_heights()))

        upper_path = obj.upper_path()
        lower_path = obj.lower_path()

        height, width = obj.geometry()

        i,j = pos
        if i < height and j < width:
            index = i+j
            if heights[j][0] == i+1:
                upper_path[index:index+2] = [1,0]
            if heights[j][1] == i:
                lower_path[index:index+2] = [0,1]
        else:
            if i == height:
                lower_path[-1:] = [0,1]
                upper_path += [0]
            else:
                lower_path += [1]
                upper_path[-1:] = [1,0]

        return ParallelogramPolyomino([lower_path, upper_path])

    def remove_cell(self, obj, pos, dirty={}):
        r"""
        Remove cell

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import ParallelogramPolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 0, 1, 1], [1, 1, 0, 0]])
            sage: ppa = ParallelogramPolyominoGridViewAdapter()
            sage: ppa.remove_cell(pp, (1, 0))
            [[0, 1, 0, 1], [1, 1, 0, 0]]
            sage: ppa.remove_cell(pp, (1, 1))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 1)' is not removable.
        """
        if pos not in self.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))

        heights = list(zip(obj.upper_heights(),obj.lower_heights()))
        upper_path = obj.upper_path()
        lower_path = obj.lower_path()
        i,j = pos
        index = i+j

        if len(heights) != j+1:
            if heights[j][0] == i:
                upper_path[index:index+2] = [0,1]
            if heights[j][1]-1 == i:
                lower_path[index:index+2] = [1,0]
        else:
            if heights[j][0] != i and heights[j][1]-1 == i:
                lower_path[index:index+2] = [1]
                upper_path.pop()
            elif heights[j][1]-1 == i:
                lower_path.pop()
                upper_path[index:index+2] = [0]
            else:
                upper_path[index:index+2] = [0,1]

        return ParallelogramPolyomino([lower_path, upper_path])


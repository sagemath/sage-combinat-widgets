# -*- coding: utf-8 -*-
r"""
Grid View Adapter for parallelogram polyominos

**Grid View parallelogram polyominos operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~PolyominoGridViewAdapter.compute_cells` | Compute parallelogram polyomino celss as a dictionary { coordinate pair : False }
    :meth:`~PolyominoGridViewAdapter.addable_cells` | List addable cells
    :meth:`~PolyominoGridViewAdapter.removable_cells` | List removable cells
    :meth:`~PolyominoGridViewAdapter.add_cell` | Add a cell
    :meth:`~PolyominoGridViewAdapter.remove_cell` | Remove a cell

AUTHORS ::

    Henri Derycke

"""
from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter

class PolyominoGridViewAdapter(GridViewAdapter):
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
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import PolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 1, 1],[1, 1 ,0]])
            sage: PolyominoGridViewAdapter.compute_cells(pp)
            {(0, 0): False, (0, 1): False}
        """
        cells = {}
        lower_heights = obj.lower_heights()
        upper_heights = obj.upper_heights()
        for i in range(obj.width()):
            for j in range(upper_heights[i],lower_heights[i]):
                cells[j,i] = False
        return cells
    
    @staticmethod
    def addable_cells(obj):
        r"""
        List object addable cells

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import PolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 1, 0, 1], [1, 1, 0, 0]])
            sage: PolyominoGridViewAdapter.addable_cells(pp)
            [(1, 0)]
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
        return cells
    
    @staticmethod
    def removable_cells(obj):
        r"""
        List object removable cells

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import PolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 0, 1, 1], [1, 1, 0, 0]])
            sage: PolyominoGridViewAdapter.removable_cells(pp)
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
            
        return cells
    
    def add_cell(self, obj, pos, val=None, dirty={}):
        r"""
        Add cell

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import PolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 1, 0, 1], [1, 1, 0, 0],])
            sage: ppa = PolyominoGridViewAdapter()
            sage: ppa.add_cell(pp, (1, 0))
            [[0, 0, 1, 1], [1, 1, 0, 0]]
            sage: ppa.add_cell(pp, (1, 1))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 1)' is not addable.
        """
        if not pos in self.addable_cells(obj):
            raise ValueError("Cell position '%s' is not addable." % str(pos))

        heights = list(zip(obj.upper_heights(),obj.lower_heights()))
        upper_path = obj.upper_path()
        lower_path = obj.lower_path()
        i,j = pos
        index = i+j
        if heights[j][0] == i+1:
            upper_path[index:index+2] = [1,0]
        if heights[j][1] == i:
            lower_path[index:index+2] = [0,1]
            
        return ParallelogramPolyomino([lower_path, upper_path])
    
    def remove_cell(self, obj, pos, dirty={}):
        r"""
        Remove cell

        TESTS ::

            sage: from sage.combinat.parallelogram_polyomino import ParallelogramPolyomino
            sage: from sage_widget_adapters.combinat.parallelogram_polyomino_grid_view_adapter import PolyominoGridViewAdapter
            sage: pp = ParallelogramPolyomino([[0, 0, 1, 1], [1, 1, 0, 0]])
            sage: ppa = PolyominoGridViewAdapter()
            sage: ppa.remove_cell(pp, (1, 0))
            [[0, 1, 0, 1], [1, 1, 0, 0]]
            sage: ppa.remove_cell(pp, (1, 1))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 1)' is not removable.
        """
        if not pos in self.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))
            
        heights = list(zip(obj.upper_heights(),obj.lower_heights()))
        upper_path = obj.upper_path()
        lower_path = obj.lower_path()
        i,j = pos
        index = i+j
        if heights[j][0] == i:
            upper_path[index:index+2] = [0,1]
        if heights[j][1]-1 == i:
            lower_path[index:index+2] = [1,0]
            
        return ParallelogramPolyomino([lower_path, upper_path])

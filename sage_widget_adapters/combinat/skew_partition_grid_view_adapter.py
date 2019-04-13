# -*- coding: utf-8 -*-
r"""
Grid View Adapter for skew partitions

**Grid View skew partition operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~SkewPartitionGridViewAdapter.cell_to_display` | Static method for typecasting cell content to widget display value
    :meth:`~SkewPartitionGridViewAdapter.display_to_cell` | Instance method for typecasting widget display value to cell content
    :meth:`~SkewPartitionGridViewAdapter.compute_cells` | Compute skew partition cells as a dictionary { coordinate pair : Integer }
    :meth:`~SkewPartitionGridViewAdapter.from_cells` | Create a new skew partition from a cells dictionary
    :meth:`~SkewPartitionGridViewAdapter.get_cell` | Get the skew partition cell content
    :meth:`~SkewPartitionGridViewAdapter.addable_cells` | List addable cells
    :meth:`~SkewPartitionGridViewAdapter.removable_cells` | List removable cells
    :meth:`~SkewPartitionGridViewAdapter.add_cell` | Add a cell
    :meth:`~SkewPartitionGridViewAdapter.remove_cell` | Remove a cell

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from sage.combinat.skew_partition import SkewPartition
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
from six import text_type


class SkewPartitionGridViewAdapter(GridViewAdapter):
    r"""
    Grid view adapter for skew partitions.

    ATTRIBUTES::
        * ``objclass`` -- SkewPartition
        * ``celltype`` -- bool
        * ``cellzero`` -- False
    """
    objclass = SkewPartition
    celltype = bool
    cellzero = False

    @staticmethod
    def cell_to_display(cell_content, display_type=bool):
        r"""
        From object cell content
        to widget display value.

        TESTS ::

            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: SkewPartitionGridViewAdapter.cell_to_display(True)
            True
            sage: from six import text_type
            sage: SkewPartitionGridViewAdapter.cell_to_display("my string", text_type)
            ''
        """
        if display_type == text_type:
            return ''
        return cell_content

    def display_to_cell(self, display_value, display_type=bool):
        r"""
        From widget cell value
        to object display content

        TESTS ::

            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: pa = SkewPartitionGridViewAdapter()
            sage: pa.display_to_cell(True)
            True
            sage: pa.display_to_cell('')
            False
        """
        if not display_value or display_type == text_type:
            return self.cellzero
        return display_value

    @staticmethod
    def compute_cells(obj):
        r"""
        From a skew partition,
        return a dictionary { coordinates pair : Integer }

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: sp = SkewPartition([[4, 2, 1],[2, 1]])
            sage: SkewPartitionGridViewAdapter.compute_cells(sp)
            {(0, 2): False, (0, 3): False, (1, 1): False, (2, 0): False}
        """
        return {(i,j):False for (i,j) in obj.cells()}

    @classmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : Integer }
        return a corresponding skew partition.

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: SkewPartitionGridViewAdapter.from_cells({(0, 2): False, (0, 3): False, (1, 1): False, (2, 0): False})
            [4, 2, 1] / [2, 1]
        """
        height = max([pos[0] for pos in cells]) + 1
        outer = [max([pos[1] for pos in cells if pos[0]==i]) + 1 for i in range(height)]
        inner = [min([pos[1] for pos in cells if pos[0]==i]) for i in \
                 range(height) if min([pos[1] for pos in cells if pos[0]==i]) > 0]
        try:
            return cls.objclass([outer,inner])
        except:
            raise TypeError(
                "This object is not compatible with this adapter (%s, for %s objects)" % (cls, cls.objclass))

    @staticmethod
    def get_cell(obj, pos):
        r"""
        Get cell value

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: sp = SkewPartition([[4, 2, 1],[2, 1]])
            sage: SkewPartitionGridViewAdapter.get_cell(sp, (1, 1))
            False
            sage: SkewPartitionGridViewAdapter.get_cell(sp, (1, 0))
            Traceback (most recent call last):
            ...
            ValueError: Cell '(1, 0)' not in object.
        """
        try:
            assert pos[0] < len(obj) and pos[1] < obj.outer()[pos[0]] and pos[1] >= obj.inner()[pos[0]]
        except:
            raise ValueError("Cell '%s' not in object." % str(pos))
        return False

    def set_cell(self, obj, pos, val, dirty={}, constructorname=''):
        r"""
        From a partition `obj`, a position (pair of coordinates) `pos` and a value `val`,
        return a new partition with a modified cell at position `pos`.
        Actually remove the cell if it's removable, otherwise return the same partition.

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: sp = SkewPartition([[7, 4, 2, 1],[2, 1, 1]])
            sage: spa = SkewPartitionGridViewAdapter()
            sage: spa.set_cell(sp, (1,6), True)
            [7, 4, 2, 1] / [2, 1, 1]
            sage: spa.set_cell(sp, (1,3), True)
            [7, 3, 2, 1] / [2, 1, 1]
        """
        if pos in self.removable_cells(obj):
            return self.remove_cell(obj, pos, dirty)
        return obj

    @staticmethod
    def addable_cells(obj):
        r"""
        List object addable cells

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: sp = SkewPartition([[4, 2, 1],[2, 1]])
            sage: SkewPartitionGridViewAdapter.addable_cells(sp)
            [(0, 1), (1, 0), (0, 4), (1, 2), (2, 1), (3, 0)]
        """
        return obj.inner().corners() + obj.outer().outside_corners()

    @staticmethod
    def removable_cells(obj):
        r"""
        List object removable cells

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: SkewPartitionGridViewAdapter.removable_cells(SkewPartition([[4, 2, 1],[2, 1]]))
            [(0, 2), (1, 1), (2, 0), (0, 3)]
            sage: SkewPartitionGridViewAdapter.removable_cells(SkewPartition([[7, 4, 2, 1],[2, 1, 1]]))
            [(0, 2), (1, 1), (3, 0), (0, 6), (1, 3), (2, 1)]
        """
        ret = obj.inner().outside_corners()
        for c in obj.outer().corners():
            if not c in ret:
                ret.append(c)
        return ret

    def add_cell(self, obj, pos, val=None, dirty={}):
        r"""
        Add cell

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: sp = SkewPartition([[7, 4, 2, 1],[2, 1, 1]])
            sage: spa = SkewPartitionGridViewAdapter()
            sage: spa.add_cell(sp, (0, 7))
            [8, 4, 2, 1] / [2, 1, 1]
            sage: spa.add_cell(sp, (2, 0))
            [7, 4, 2, 1] / [2, 1]
            sage: spa.add_cell(sp, (4, 0))
            [7, 4, 2, 1, 1] / [2, 1, 1]
            sage: spa.add_cell(sp, (2, 3))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(2, 3)' is not addable.
        """
        if not pos in self.addable_cells(obj):
            raise ValueError("Cell position '%s' is not addable." % str(pos))
        try:
            if pos in obj.outer().outside_corners():
                return self.objclass([obj.outer().add_cell(pos[0]), obj.inner()])
            else:
                return self.objclass([obj.outer(), obj.inner().remove_cell(pos[0])])
        except:
            raise ValueError("Error adding cell %s to %s" % (pos, self.objclass))

    def remove_cell(self, obj, pos, dirty={}):
        r"""
        Remove cell

        TESTS ::

            sage: from sage.combinat.skew_partition import SkewPartition
            sage: from sage_widget_adapters.combinat.skew_partition_grid_view_adapter import SkewPartitionGridViewAdapter
            sage: sp = SkewPartition([[7, 4, 2, 1],[2, 1, 1]])
            sage: spa = SkewPartitionGridViewAdapter()
            sage: spa.remove_cell(sp, (0, 6))
            [6, 4, 2, 1] / [2, 1, 1]
            sage: spa.remove_cell(sp, (1, 1))
            [7, 4, 2, 1] / [2, 2, 1]
            sage: spa.remove_cell(sp, (1, 2))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 2)' is not removable.
        """
        if not pos in self.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))
        try:
            if pos in obj.outer().corners():
                return self.objclass([obj.outer().remove_cell(pos[0]), obj.inner()])
            else:
                return self.objclass([obj.outer(), obj.inner().add_cell(pos[0])])
        except:
            raise ValueError("Error removing cell %s from %s" % (pos, self.objclass))

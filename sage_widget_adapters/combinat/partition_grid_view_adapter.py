# -*- coding: utf-8 -*-
r"""
Grid View Adapter for partitions

**Grid View partition operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~PartitionGridViewAdapter.cell_to_display` | Static method for typecasting cell content to widget display value
    :meth:`~PartitionGridViewAdapter.display_to_cell` | Instance method for typecasting widget display value to cell content
    :meth:`~PartitionGridViewAdapter.compute_cells` | Compute partition cells as a dictionary { coordinate pair : Integer }
    :meth:`~PartitionGridViewAdapter.from_cells` | Create a new partition from a cells dictionary
    :meth:`~PartitionGridViewAdapter.get_cell` | Get the partition cell content
    :meth:`~PartitionGridViewAdapter.addable_cells` | List addable cells
    :meth:`~PartitionGridViewAdapter.removable_cells` | List removable cells
    :meth:`~PartitionGridViewAdapter.add_cell` | Add a cell
    :meth:`~PartitionGridViewAdapter.remove_cell` | Remove a cell

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from sage.combinat.partition import Partition
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
from six import text_type

class PartitionGridViewAdapter(GridViewAdapter):
    r"""
    Grid view adapter for partitions.

    ATTRIBUTES::
        * ``objclass`` -- Partition
        * ``celltype`` -- bool
        * ``cellzero`` -- False
    """
    objclass = Partition
    constructorname = 'Partition'
    celltype = bool
    cellzero = False

    @staticmethod
    def cell_to_display(cell_content, display_type=bool):
        r"""
        From object cell content
        to widget display value.

        TESTS ::

            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: PartitionGridViewAdapter.cell_to_display(True)
            True
            sage: from six import text_type
            sage: PartitionGridViewAdapter.cell_to_display("my string", text_type)
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

            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: pa = PartitionGridViewAdapter()
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
        From a partition,
        return a dictionary { coordinates pair : Integer }

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([3, 2, 1, 1])
            sage: PartitionGridViewAdapter.compute_cells(p)
            {(0, 0): False,
            (0, 1): False,
            (0, 2): False,
            (1, 0): False,
            (1, 1): False,
            (2, 0): False,
            (3, 0): False}
        """
        return {(i,j):False for (i,j) in obj.cells()}

    @classmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : Integer }
        return a corresponding partition

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: PartitionGridViewAdapter.from_cells({(0, 0): False, (0, 1): False, (0, 2): True, (0, 3): False, (1, 0): False, (2, 0): True})
            [4, 1, 1]
        """
        partition_elements = [
            len([(i, pos[1]) for pos in cells if pos[0] == i]) for i in range(max(pos[0] for pos in cells) + 1)]
        try:
            return cls.objclass(partition_elements)
        except:
            raise TypeError(
                "This object is not compatible with this adapter (%s, for %s objects)" % (cls, cls.objclass))

    @staticmethod
    def get_cell(obj, pos):
        r"""
        Get cell value

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([6, 5, 2, 1])
            sage: PartitionGridViewAdapter.get_cell(p, (1, 1))
            False
            sage: PartitionGridViewAdapter.get_cell(p, (1, 6))
            Traceback (most recent call last):
            ...
            ValueError: Cell '(1, 6)' not in partition.
        """
        try:
            assert pos[0] < len(obj) and pos[1] < obj[pos[0]]
        except:
            raise ValueError("Cell '%s' not in partition." % str(pos))
        return False

    def set_cell(self, obj, pos, val, dirty={}, constructorname=''):
        r"""
        From a partition `obj`, a position (pair of coordinates) `pos` and a value `val`,
        return a new partition with a modified cell at position `pos`.
        Remove the cell if relevant, otherwise return the same partition.

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([6, 5, 2, 1])
            sage: pa = PartitionGridViewAdapter()
            sage: pa.set_cell(p, (1,2), True)
            [6, 5, 2, 1]
            sage: pa.set_cell(p, (1,4), True)
            [6, 4, 2, 1]
        """
        if pos in self.removable_cells(obj) and val:
            return self.remove_cell(obj, pos, dirty)
        return obj

    @staticmethod
    def addable_cells(obj):
        r"""
        List object addable cells

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([6, 5, 2, 1])
            sage: PartitionGridViewAdapter.addable_cells(p)
            [(0, 6), (1, 5), (2, 2), (3, 1), (4, 0)]
        """
        return obj.outside_corners()

    @staticmethod
    def removable_cells(obj):
        r"""
        List object removable cells

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([6, 5, 2, 1])
            sage: PartitionGridViewAdapter.removable_cells(p)
            [(0, 5), (1, 4), (2, 1), (3, 0)]
        """
        return obj.corners()

    def add_cell(self, obj, pos, val=None, dirty={}):
        r"""
        Add cell

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([6, 5, 2, 1])
            sage: pa = PartitionGridViewAdapter()
            sage: pa.add_cell(p, (2, 2))
            [6, 5, 3, 1]
            sage: pa.add_cell(p, (4, 0), 42)
            [6, 5, 2, 1, 1]
            sage: pa.add_cell(p, (2, 0))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(2, 0)' is not addable.
        """
        if not pos in self.addable_cells(obj):
            raise ValueError("Cell position '%s' is not addable." % str(pos))
        try:
            return obj.add_cell(pos[0])
        except Exception as e:
            return e

    def remove_cell(self, obj, pos, dirty={}):
        r"""
        Remove cell

        TESTS ::

            sage: from sage.combinat.partition import Partition
            sage: from sage_widget_adapters.combinat.partition_grid_view_adapter import PartitionGridViewAdapter
            sage: p = Partition([6, 5, 2, 1])
            sage: pa = PartitionGridViewAdapter()
            sage: pa.remove_cell(p, (2, 1))
            [6, 5, 1, 1]
            sage: pa.remove_cell(p, (1, 1))
            Traceback (most recent call last):
            ...
            ValueError: Cell position '(1, 1)' is not removable.
        """
        if not pos in self.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))
        try:
            return obj.remove_cell(pos[0])
        except Exception as e:
            return e

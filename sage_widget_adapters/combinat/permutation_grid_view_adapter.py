# -*- coding: utf-8 -*-
r"""
Grid View Adapter for permutations

**Grid View permutation operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~PermutationGridViewAdapter.cell_to_display` | Static method for typecasting cell content to widget display value
    :meth:`~PermutationGridViewAdapter.display_to_cell` | Instance method for typecasting widget display value to cell content
    :meth:`~PermutationGridViewAdapter.compute_cells` | Compute permutation cells as a dictionary { coordinate pair : Integer }
    :meth:`~PermutationGridViewAdapter.from_cells` | Create a new permutation from a cells dictionary
    :meth:`~PermutationGridViewAdapter.get_cell` | Get the permutation cell content
    :meth:`~PermutationGridViewAdapter.addable_cells` | List addable cells
    :meth:`~PermutationGridViewAdapter.removable_cells` | List removable cells
    :meth:`~PermutationGridViewAdapter.add_cell` | Add a cell
    :meth:`~PermutationGridViewAdapter.remove_cell` | Remove a cell

AUTHORS: Odile Bénassy, Nicolas Thiéry

"""
from sage.combinat.permutation import *
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
from six import text_type

class PermutationGridViewAdapter(GridViewAdapter):
    r"""
    Grid view adapter for permutations.

    ATTRIBUTES::
        * ``objclass`` -- Permutation
        * ``celltype`` -- bool
        * ``cellzero`` -- False
    """
    objclass = Permutation
    #constructorname = 'Permutation'
    celltype = bool
    cellzero = False

    @staticmethod
    def compute_cells(obj):
        r"""
        From a permutation,
        return a dictionary { coordinates pair : Integer }

        TESTS::
            sage: from sage.combinat.permutation import Permutation
            sage: from sage_widget_adapters.combinat.permutation_grid_view_adapter import PermutationGridViewAdapter
            sage: p = Permutation([2, 3, 4, 5, 1])
            sage: PermutationGridViewAdapter.compute_cells(p)
            {(0, 0): 2, (0, 1): 3, (0, 2): 4, (0, 3): 5, (0, 4): 1}
        """
        return {(0,i):obj[i] for i in range(len(obj))}

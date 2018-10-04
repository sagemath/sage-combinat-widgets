# -*- coding: utf-8 -*-
r"""
Generic Grid View Adapter

**Grid View operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GridViewAdapter.cell_to_unicode` | Static method for typecasting cell content to unicode
    :meth:`~GridViewAdapter.unicode_to_cell` | Static method for typecasting unicode to cell content
    :meth:`~GridViewAdapter.compute_cells` | Compute object cells as a dictionary { coordinate pair : integer }
    :meth:`~GridViewAdapter.from_cells` | Create a new Sage object from a cells dictionary
    :meth:`~GridViewAdapter._validate` | Validate a new object
    :meth:`~GridViewAdapter.get_cell` | Get the object cell content
    :meth:`~GridViewAdapter.set_cell` | Set the object cell content
"""
from sage.all import SageObject
from traitlets import Any

class GridViewAdapter:
    objclass = SageObject
    traitclass = Any

    @staticmethod
    def cell_to_unicode(cell_content):
        return str(cell_content)

    @staticmethod
    def unicode_to_cell(s):
        raise NotImplementedError

    @staticmethod
    def compute_cells(obj):
        r"""
        From an object `obj`,
        return a dictionary { coordinates pair : integer }
        This method must be implemented in subclasses.
        """
        raise NotImplementedError

    @classmethod
    def _validate(cls, obj):
        r"""
        From an object `obj`,
        Try to build an object of type `cls`.
        TESTS:
        sage: from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
        sage: GridViewAdapter._validate(pi)
        """
        try:
            new_value = cls.objclass(obj)
        except:
            raise TypeError("This object is not compatible with this adapter (%s, for %s objects)" % (cls, objclass))

    @staticmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : integer }
        return a Sage object.
        This method must be implemented in subclasses.
        """
        raise NotImplementedError

    @staticmethod
    def get_cell(obj, pos):
        r"""
        From an object and a tuple `pos`,
        return the object cell value at position `pos`.
        This method must be implemented in subclasses.
        """
        raise NotImplementedError

    @staticmethod
    def set_cell(obj, pos, val):
        r"""
        From an object, tuple `pos` and a value `val`,
        return a new Sage object
        with a modified cell at position pos.
        This method must be implemented in subclasses.
        """
        raise NotImplementedError

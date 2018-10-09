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

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
from sage.all import SageObject
import traitlets
from sage.misc.abstract_method import abstract_method

class GridViewAdapter:
    objclass = SageObject
    cellclass = None
    traitclass = traitlets.Instance
    traitclass_default_value = traitlets.Undefined

    @staticmethod
    def cell_to_unicode(cell_content):
        r"""
        From a cell value `cell_content`,
        return matching unicode string.
        """
        return str(cell_content)

    @classmethod
    def unicode_to_cell(cls, s):
        r"""
        From an unicode string `s`,
        return matching cell value.
        """
        return cls.cellclass(s)

    @staticmethod
    @abstract_method
    def compute_cells(obj):
        r"""
        From an object `obj`,
        return a dictionary { coordinates pair : integer }
        """

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
            raise TypeError("This object is not compatible with this adapter (%s, for %s objects)" % (cls, cls.objclass))

    @classmethod
    @abstract_method
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : integer }
        return a Sage object.
        """

    @staticmethod
    @abstract_method
    def get_cell(obj, pos):
        r"""
        From an object and a tuple `pos`,
        return the object cell value at position `pos`.
        """

    @classmethod
    @abstract_method
    def set_cell(cls, obj, pos, val):
        r"""
        From a Sage object, a position (pair of coordinates) `pos` and a value `val`,
        return a new Sage object.
        with a modified cell at position `pos`.
        """

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

    @classmethod
    @abstract_method(optional = True)
    def add_cell(obj, cls, pos, val):
        r"""
        If possible, add a cell to object `obj`
        at position `pos` and with value `val`.
        """

    @classmethod
    @abstract_method(optional = True)
    def remove_cell(cls, obj, pos):
        r"""
        If possible, remove a cell from object `obj`
        at position `pos`.
        """

    @classmethod
    @abstract_method(optional = True)
    def append_row(cls, obj, r=None):
        r"""
        If possible, append a row to object `obj`
        with values from list `r`.
        """

    @classmethod
    @abstract_method(optional = True)
    def insert_row(obj, index, r=None):
        r"""
        If possible, insert a row to object `obj`
        at index `index`, with values from list `r`.
        """

    @classmethod
    @abstract_method(optional = True)
    def remove_row(cls, obj, index=None):
        r"""
        If possible, remove a row from object `obj`
        at index `index`.
        """

    @classmethod
    @abstract_method(optional = True)
    def append_column(cls, obj, r=None):
        r"""
        If possible, append a column to object `obj`
        with values from list `r`.
        """

    @classmethod
    @abstract_method(optional = True)
    def insert_column(cls, obj, index, r=None):
        r"""
        If possible, insert a column to object `obj`
        at index `index`, with values from list `r`.
        """

    @classmethod
    @abstract_method(optional = True)
    def remove_column(cls, obj, index=None):
        r"""
        If possible, remove a column from object `obj`
        at index `index`.
        """

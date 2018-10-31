# -*- coding: utf-8 -*-
r"""
Generic Geometric View Adapter

**Geometric View operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GeometricViewAdapter.unicode_to_cell` | Static method for typecasting unicode to cell content
    :meth:`~GeometricViewAdapter.compute_cells` | Compute object cells as a dictionary { coordinate pair : Integer }
    :meth:`~GeometricViewAdapter.from_cells` | Create a new object from a cells dictionary
    :meth:`~GeometricViewAdapter.get_cell` | Get the object cell content
    :meth:`~GeometricViewAdapter.set_cell` | Set the object cell content

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
import traitlets
from sage.misc.abstract_method import abstract_method
from sage.all import SageObject
from sage.graphs.digraph import DiGraph

class VerticesPath(DiGraph):
    r"""
    A path on a solid, defined by a suite of vertices.
    """
    def __init__(self, points):
        r"""
        Define a path from a list of points
        """
        self.vertices = points

    def is_closed(self):
        return (self.vertices[0] == self.vertices[-1])

    def append_vertex(self, point):
        pass

    def drop_vertex(self, point):
        pass

class GeometricViewAdapter(object):
    objclass = SageObject
    traitclass = traitlets.Instance

    @staticmethod
    def cell_to_unicode(cell_content):
        r"""
        From a cell value `cell_content`,
        return matching unicode string.
        """
        return str(cell_content)

    def unicode_to_cell(self, s):
        r"""
        From an unicode string `s`,
        return matching cell value.
        """
        if s:
            return self.celltype(s)
        return self.cellzero

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
        sage: from sage_widget_adapters.generic_geometric_view_adapter import GeometricViewAdapter
        sage: GeometricViewAdapter._validate(pi)
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

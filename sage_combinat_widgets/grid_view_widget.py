# -*- coding: utf-8 -*-
r"""
An editable GridViewWidget for Sage Jupyter Notebook

EXAMPLES ::
    sage: from sage_combinat_widgets import GridViewWidget
    sage: from sage.all import matrix, graphs
    sage: m = matrix([[1,2], [3,4]])
    sage: w = GridViewWidget(m)
    sage: g = graphs.GridGraph((3,3))
    sage: w = GridViewWidget(g)

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
from __future__ import print_function, absolute_import
from six import add_metaclass
from sage.misc.bindable_class import BindableClass
from sage.combinat.tableau import *
from sage.all import SageObject, matrix, Integer
from sage.rings.real_mpfr import RealLiteral
from sage.graphs.generic_graph import GenericGraph
import traitlets

SAGETYPES_TO_TRAITTYPES = {
    bool: traitlets.Bool,
    int: traitlets.Integer,
    float: traitlets.Float,
    list: traitlets.List,
    set: traitlets.Set,
    dict: traitlets.Dict,
    Integer: traitlets.Integer,
    RealLiteral: traitlets.Float
    }


import sage.misc.classcall_metaclass
class MetaHasTraitsClasscallMetaclass(traitlets.MetaHasTraits, sage.misc.classcall_metaclass.ClasscallMetaclass):
    pass
@add_metaclass(MetaHasTraitsClasscallMetaclass)
class BindableClassWithMeta(BindableClass):
    pass
class BindableWidgetClass(traitlets.HasTraits, BindableClassWithMeta):
    pass

class GridViewWidget(BindableWidgetClass):
    r"""Base Jupyter Interactive Widget for Sage Grid Objects

    Composed of cells. No decision made here about cell representation.
    The cell trait objects will store values
    that are refered to through object cells as a dictionary
    with coordinates (row_number, cell_number_in_row) as keys
    """
    value = traitlets.Any()

    def __init__(self, obj, **kwargs):
        r"""
        TESTS::

            sage: from sage_combinat_widgets import GridViewWidget
            sage: from sage.all import matrix, graphs
            sage: from sage.graphs.generic_graph import GenericGraph
            sage: v = vector((1,2,3))
            sage: w = GridViewWidget(v)
            sage: g = graphs.AztecDiamondGraph(3)
            sage: w = GridViewWidget(g)
            sage: t = StandardTableaux(5).random_element()
            sage: w = GridViewWidget(t)
            sage: f = x^5
            sage: w = GridViewWidget(f)
            TypeError
        """
        try:
            cells = list(obj)
        except:
            raise TypeError("This object cannot be represented by a GridViewWidget")
        super(GridViewWidget, self).__init__()
        self.value = obj
        self.compute_cells()

    def validate(self, obj, value):
        return issubclass(obj.__class__, SageObject)

    def compute_cells(self, obj=None):
        r"""We have an object value
        but we want to compute cells
        as a dictionary (row_number, cell_number_in_row) -> trait
        The cell_trait_class will depend on the object
        """
        if not obj:
            obj = self.value
        if not obj:
            return
        cells = []
        if issubclass(obj.__class__, GenericGraph): # i.e. a graph
            cells = [((i,j), None) for (i,j) in obj.vertices()]
            trait_class = traitlets.Instance
        elif hasattr(obj, 'cells'): # e.g. a tableau
            cells = [((i,j), obj[i][j]) for (i,j) in obj.cells()]
            trait_class = traitlets.Integer
        elif hasattr(obj, 'nrows'): # e.g. a matrix
            cells = [((i, j), obj[i][j]) for i in range(obj.nrows()) for j in range(obj.ncols())]
            if type(obj[0][0]) in SAGETYPES_TO_TRAITTYPES:
                trait_class = SAGETYPES_TO_TRAITTYPES[type(obj[0][0])]
            else:
                trait_class = traitlets.Instance
        elif hasattr(obj, 'row'): # e.g. a vector
            cells = [((i, j), obj[i+j]) for i in range(matrix(obj).nrows()) for j in range(matrix(obj).ncols())]
            if type(obj[0]) in SAGETYPES_TO_TRAITTYPES:
                trait_class = SAGETYPES_TO_TRAITTYPES[type(obj[0])]
            else:
                trait_class = traitlets.Instance
        else:
            cells = []
            trait_class = traitlets.Instance
        self.cells = {}
        for pos, val in cells:
            self.cells[pos] = val
            traitname = 'cell_%d_%d' % pos
            if not self.has_trait(traitname):
                self.add_traits(**{traitname : trait_class()})

    def get_value(self):
        return self.value

    def set_value(self, obj):
        self.value = obj
        self.compute()

    def get_cells(self):
        return self.cells

    def set_value_from_cells(self, obj_class=None, cells=None):
        r"""We have an object value, but we want to change it according to cells
        Yet we want to keep the same class (or warn if that's impossible)
        INPUT::
        * an object class (by default: self.value.__class__)
        * a cells dictionary (i,j)->val (by default: self.cells)
        """
        if not obj_class and self.value:
            obj_class = self.value.__class__
        if not obj_class:
            return
        if not cells:
            cells = self.cells
        if not cells:
            return
        if issubclass(obj.__class__, GenericGraph): # i.e. a graph
            g = obj_class()
            g.add_vertices(list(cells.keys()))
            self.value = g
        elif hasattr(obj_class, 'cells') or hasattr(obj_class, 'rows'): # e.g. a tableau / matrix / vector
            positions = cells.keys()
            positions.sort()
            self.value = obj_class([[cells[pos] for pos in positions if pos[0]==i] for i in uniq([t[0] for t in positions])])
        else:
            raise TypeError("Unable to cast the object into a grid-like one.")

    def edit_cell(self, pos, val):
        self.cells[pos] = val
        self.set_value_from_cells()

    def add_cell(self, pos, val):
        self.cells[pos] = val
        traitname = 'cell_%d_%d' % pos
        for pos in self.cells:
            trait_class = getattr(self, 'cell_%d_%d' % pos).__class__
            break
        if not self.has_trait(traitname):
            self.add_traits(**{traitname : trait_class()})
        if issubclass(obj.__class__, GenericGraph): # i.e. a graph
            self.value.add_vertex(pos)
        else:
            self.set_value_from_cells()

    def remove_cell(self, pos):
        del self.cells[pos]
        if self.has_trait(traitname):
            delattr(self, traitname)
            del self._trait_values[traitname]
        if hasattr(self.value, 'vertices'): # e.g. a graph
            self.value.delete_vertex(pos)
        else:
            self.set_value_from_cells()

    def addable_cells(self):
        if hasattr(self.value, 'cells'): # e.g. a tableau
            return self.value.shape().outside_corners()

    def removable_cells(self):
        if hasattr(self.value, 'cells'): # e.g. a tableau
            return self.value.corners()

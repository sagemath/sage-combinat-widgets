# -*- coding: utf-8 -*-
r"""
An editable GridViewEditor for Sage Jupyter Notebook

EXAMPLES ::
    sage: from sage_combinat_widgets import GridViewEditor
    sage: from sage_widget_adapters import *
    sage: t = StandardTableau([[1, 2, 5, 6], [3], [4]])
    sage: tg = TableauGridViewAdapter(t.parent(), t)
    sage: w = GridViewEditor(tg)
    sage: from sage.graphs.generators.basic import GridGraph
    sage: gg = GraphGridViewAdapter()
    sage: w = GridViewEditor(gg)

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
from sage.combinat.partition import Partition
from sage.structure.list_clone import ClonableList
import traitlets
from sage_widget_adapters import *

SAGETYPE_TO_TRAITTYPE = {
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
class BindableEditorClass(traitlets.HasTraits, BindableClassWithMeta):
    pass

class GridViewEditor(BindableEditorClass):
    r"""Base Editor for grid-representable Sage Objects

    Composed of cells. No decision made here about cell representation.
    The cell trait objects will store values
    that are refered to through object cells as a dictionary
    with coordinates (row_number, cell_number_in_row) as keys
    """
    value = traitlets.Any()

    def __init__(self, obj):
        r"""
        TESTS::

            sage: from sage_combinat_widgets import GridViewEditor
            sage: from sage.all import matrix, graphs
            sage: from sage.graphs.generic_graph import GenericGraph
            sage: v = vector((1,2,3))
            sage: w = GridViewEditor(v)
            sage: g = graphs.AztecDiamondGraph(3)
            sage: w = GridViewEditor(g)
            sage: t = StandardTableaux(5).random_element()
            sage: w = GridViewEditor(t)
            sage: f = x^5
            sage: w = GridViewEditor(f)
            TypeError
        """
        try:
            cells = list(obj)
        except:
            raise TypeError("Is this object really grid-representable?")
        super(GridViewEditor, self).__init__()
        self.set_value(obj)

    def validate(self, obj, value=None, obj_class=None):
        r"""
        Validate the object type
        """
        if obj_class:
            return issubclass(obj.__class__, obj_class)
        try:
            cells = list(obj)
        except:
            raise TypeError("Is this object really grid-representable?")
        return issubclass(obj.__class__, SageObject)

    def compute(self, obj=None):
        r"""We have an object value
        but we want to compute cells
        as a dictionary (row_number, cell_number_in_row) -> trait
        The cell traitclass will depend on the object
        """
        if not obj:
            obj = self.value
        if not obj:
            return
        try:
            self.cells = obj.compute_cells() # Could also be self.adapter.compute_cells(obj)
        except:
            print("Cannot find an Adapter for this object")
            self.cells = {}
        if hasattr(obj, 'traitclass'):
            traitclass = obj.traitclass
        else:
            obj_class = obj.__class__
            if issubclass(obj_class, GenericGraph): # i.e. a graph
                traitclass = traitlets.Unicode
            elif issubclass(obj_class, Partition): # a Partition
                traitclass = traitlets.Unicode
            elif issubclass(obj_class, ClonableList): # e.g. a tableau
                traitclass = traitlets.Integer
            elif hasattr(obj, 'nrows'): # e.g. a matrix
                if type(obj[0][0]) in SAGETYPE_TO_TRAITTYPE:
                    traitclass = SAGETYPE_TO_TRAITTYPE[type(obj[0][0])]
                else:
                    traitclass = traitlets.Instance
            elif hasattr(obj, 'row'): # e.g. a vector
                if not self.cells:
                    cells = [((i, j), obj[i+j]) for i in range(matrix(obj).nrows()) for j in range(matrix(obj).ncols())]
                    for pos, val in cells:
                        self.cells[pos] = val
                if type(obj[0]) in SAGETYPE_TO_TRAITTYPE:
                    traitclass = SAGETYPE_TO_TRAITTYPE[type(obj[0])]
            else:
                traitclass = traitlets.Instance
        for pos, val in self.cells.items():
            traitname = 'cell_%d_%d' % pos
            traitvalue = val or ''
            if traitname in self._trait_values:
                self._trait_values[traitname] = traitvalue
            else:
                trait = traitclass(traitvalue)
                trait.class_init(self.__class__, traitname)
                trait.name = traitname
                trait.instance_init(self)
                trait.value = traitvalue
                #self._trait_values[traitname] = traitvalue # Is set by instance_init()
        self.traitclass = traitclass

    def get_value(self):
        return self.value

    def set_value(self, obj):
        if not self.validate(obj):
            raise ValueError("Object %s is not compatible." % str(obj))
        self.value = obj # FIXME here try to find the relevant Adapter
        self.compute()

    def get_cells(self):
        return self.cells

    def set_value_from_cells(self, obj_class=None, cells={}):
        r"""We have an object value, but we want to change it according to cells
        Yet we want to keep the same class (or warn if that's impossible)
        INPUT::
        * an object class (by default: self.value.__class__)
        * a cells dictionary (i,j)->val
        """
        if not obj_class and self.value:
            obj_class = self.value.__class__
        if not obj_class:
            return
        if hasattr(self.value, 'from_cells'):
            try:
                obj = self.value.from_cells(cells)
            except:
                raise ValueError("Could not make an object of class '%s' from given cells" % str(obj_class))
        elif hasattr(obj_class, 'cells') or hasattr(obj_class, 'rows'): # e.g. a tableau / matrix / vector
            positions = sorted(list(cells.keys()))
            for cl in obj_class.__mro__:
                try:
                    obj = cl([[cells[pos] for pos in positions if pos[0]==i] for i in uniq([t[0] for t in positions])])
                except:
                    print("These cells cannot be turned into a %s" % cl)
        else:
            raise TypeError("Unable to cast the given cells into a grid-like object.")
        if not self.validate(obj, None, obj_class):
            raise ValueError("Could not make a compatible ('%s')  object from given cells" % str(obj_class))
        self.set_value(obj)

    def set_cell(self, pos, val):
        obj = copy(self.value)
        obj.set_cell(pos, val)
        self.set_value(obj)

    def addable_cells(self):
        return self.value.addable_cells()

    def removable_cells(self):
        return self.value.removable_cells()

    def add_cell(self, pos, val):
        if not hasattr(self.value, 'add_cell'):
            raise TypeError("Cannot add cell to this object.")
        obj = copy(self.value)
        try:
            obj.add_cell(pos, val)
        except:
            raise ValueError("Unable to add cell (position=%s and value=%s)" % (str(pos), str(val)))
        if not self.validate(obj):
            raise ValueError("This new object is not compatible with editor object class (%s)" % self.value.__class__)
        self.cells[pos] = val
        traitname = 'cell_%d_%d' % pos
        traitvalue = val
        if self.has_trait(traitname):
            trait = self.traits[traitname]
            del(trait)
            del(self.traits[traitname])
        trait = traitclass(traitvalue)
        trait.instance_init(self)
        self._trait_values[self.name] = trait.value # Can be val, or can be trait's default value
        self.value = obj

    def remove_cell(self, pos):
        if not hasattr(self.value, 'add_cell'):
            raise TypeError("Cannot add cell to this object.")
        obj = copy(self.value)
        try:
            obj.add_cell(pos, val)
        except:
            raise ValueError("Unable to add cell (position=%s and value=%s)" % (str(pos), str(val)))
        if not self.validate(obj):
            raise ValueError("This new object is not compatible with editor object class (%s)" % self.value.__class__)
        del(self.cells[pos])
        traitname = 'cell_%d_%d' % pos
        traitvalue = val
        if self.has_trait(traitname):
            trait = self.traits[traitname]
            del(trait)
            del(self.traits[traitname])
            delattr(self, traitname)
            del(self._trait_values[traitname])
        self.value = obj

    def append_row(self, r=None):
        if not hasattr(self.value, 'append_row'):
            raise TypeError("Cannot append row to this object.")
        obj = copy(self.value)
        try:
            obj.append_row(r)
        except:
            raise ValueError("Unable to append row")
        self.set_value(obj) # Will take care of everything

    def insert_row(self, index, r=None):
        if not hasattr(self.value, 'insert_row'):
            raise TypeError("Cannot insert row to this object.")
        obj = copy(self.value)
        try:
            obj.insert_row(index, r)
        except:
            raise ValueError("Unable to insert row")
        self.set_value(obj) # Will take care of everything

    def remove_row(self, index=None):
        if not hasattr(self.value, 'remove_row'):
            raise TypeError("Cannot remove row from this object.")
        obj = copy(self.value)
        try:
            obj.remove_row(index)
        except:
            raise ValueError("Unable to remove row")
        self.set_value(obj) # Will take care of everything

    def append_column(self, r=None):
        if not hasattr(self.value, 'append_column'):
            raise TypeError("Cannot append column to this object.")
        obj = copy(self.value)
        try:
            obj.append_column(r)
        except:
            raise ValueError("Unable to append column")
        self.set_value(obj) # Will take care of everything

    def insert_column(self, index, r=None):
        if not hasattr(self.value, 'insert_column'):
            raise TypeError("Cannot insert column to this object.")
        obj = copy(self.value)
        try:
            obj.insert_column(index, r)
        except:
            raise ValueError("Unable to insert column")
        self.set_value(obj) # Will take care of everything

    def remove_column(self, index=None):
        if not hasattr(self.value, 'remove_column'):
            raise TypeError("Cannot remove column from this object.")
        obj = copy(self.value)
        try:
            obj.remove_column(index)
        except:
            raise ValueError("Unable to remove column")
        self.set_value(obj) # Will take care of everything

# -*- coding: utf-8 -*-
r"""
An editable GridViewEditor for Sage Jupyter Notebook

EXAMPLES ::
    sage: from sage_combinat_widgets import GridViewEditor
    sage: t = StandardTableau([[1, 2, 5, 6], [3], [4]])
    sage: w = GridViewEditor(t)
    sage: from sage.graphs.generators.basic import GridGraph
    sage: g = GridGraph((4,3))
    sage: w = GridViewEditor(g)

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
import re, traitlets
from six import add_metaclass
from copy import copy
from sage.misc.bindable_class import BindableClass
from sage.combinat.tableau import *
from sage.all import SageObject, matrix, Integer
from sage.rings.real_mpfr import RealLiteral
from sage.graphs.graph import Graph
from sage.combinat.partition import Partition
from sage.structure.list_clone import ClonableList

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

def simplecast(x):
    r"""
    From Sage math objects to ordinary python types.
    TESTS::
        sage: from sage_combinat_widgets.grid_view_editor import simplecast
        sage: a = 1
        sage: type(simplecast(a))
        <class 'int'>
    """
    if type(x) == sage.rings.integer.Integer:
        return int(x)
    if type(x) == sage.rings.real_mpfr.RealLiteral:
        return float(x)
    return x

def extract_coordinates(s):
    r"""
    TESTS::
        sage: from sage_combinat_widgets.grid_view_editor import extract_coordinates
        sage: extract_coordinates('add_0_4')
        (0, 4)
    """
    patt = re.compile('_([0-9]+)_([0-9]+)')
    m = patt.search(s)
    if m:
        return tuple(int(i) for i in m.groups())

def get_adapter(cls):
    from sage.combinat.tableau import Tableau
    if issubclass(cls, Tableau):
        from sage_widget_adapters.combinat.tableau_grid_view_adapter import TableauGridViewAdapter
        return TableauGridViewAdapter
    from sage.matrix.matrix2 import Matrix
    if issubclass(cls, Matrix):
        from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        return MatrixGridViewAdapter
    from sage.graphs.graph import Graph
    if issubclass(cls, Graph):
        from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
        return GraphGridViewAdapter

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

    def __init__(self, obj, adapter=None):
        r"""
        TESTS::

            sage: from sage_combinat_widgets import GridViewEditor
            sage: from sage.all import matrix, graphs
            sage: from sage.graphs.generic_graph import GenericGraph
            sage: g = graphs.AztecDiamondGraph(3)
            sage: w = GridViewEditor(g)
            sage: t = StandardTableaux(5).random_element()
            sage: w = GridViewEditor(t)
            sage: f = x^5
            sage: v = vector((1,2,3))
            sage: w = GridViewEditor(v) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: Cannot find an Adapter for this object (<class 'sage.modules.vector_integer_dense.Vector_integer_dense'>)
            sage: w = GridViewEditor(f) # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            ...
            TypeError: Is this object really grid-representable?
        """
        try:
            cells = list(obj)
        except:
            raise TypeError("Is this object really grid-representable?")
        super(GridViewEditor, self).__init__()
        if adapter:
            self.adapter = adapter
        else:
            self.adapter = get_adapter(obj.__class__)
        if not self.adapter:
            raise TypeError("Cannot find an Adapter for this object (%s)" % obj.__class__)
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
            self.cells = self.adapter.compute_cells(obj)
        except:
            print("Cannot compute cells for this object")
            self.cells = {}
        if hasattr(obj, 'traitclass'):
            traitclass = obj.traitclass
        else:
            obj_class = obj.__class__
            if issubclass(obj_class, Graph): # a graph
                traitclass = traitlets.Any
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
                        self.cells[pos] = val or traitclass.default_value
                if type(obj[0]) in SAGETYPE_TO_TRAITTYPE:
                    traitclass = SAGETYPE_TO_TRAITTYPE[type(obj[0])]
            else:
                traitclass = traitlets.Instance
        traits_to_add = {}
        for pos in self.addable_cells():
            # Empty traits for addable cells
            emptytraitname = 'add_%d_%d' % pos
            emptytrait = traitclass(traitclass.default_value)
            emptytrait.name = emptytraitname
            traits_to_add[emptytraitname] = emptytrait
        for pos, val in self.cells.items():
            traitname = 'cell_%d_%d' % pos
            # Simple type casting, e.g. sage.rings.integer.Integer -> int ...
            traitvalue = simplecast(val)
            if traitname in self._trait_values:
                self._trait_values[traitname] = traitvalue
            else:
                trait = traitclass(traitvalue)
                trait.name = traitname
                traits_to_add[traitname] = trait
        self.traitclass = traitclass
        self.add_traits(**traits_to_add)

    def draw(self):
        pass

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
        if hasattr(self.adapter, 'from_cells'):
            try:
                obj = self.adapter.from_cells(cells)
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

    @traitlets.observe(traitlets.All)
    def set_cell(self, change):
        if not change.name.startswith('cell_'):
            return
        if change.new == change.old:
            return
        pos = extract_coordinates(change.name)
        val = change.new
        obj = copy(self.value)
        obj.set_cell(pos, val)
        self.set_value(obj)

    def addable_cells(self):
        if hasattr(self.adapter, 'addable_cells'):
            return self.adapter.addable_cells(self.value)
        return []

    def removable_cells(self):
        if hasattr(self.adapter, 'removable_cells'):
            return self.adapter.removable_cells(self.value)
        return []

    @traitlets.observe(traitlets.All)
    def add_cell(self, change):
        if not change.name.startswith('add_'):
            return
        pos = extract_coordinates(change.name)
        val = change.new
        if not hasattr(self.adapter, 'add_cell'):
            raise TypeError("Cannot add cell to this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.add_cell(obj, pos, val)
        except:
            raise ValueError("Unable to add cell (position=%s and value=%s)" % (str(pos), str(val)))
        if not self.validate(obj):
            raise ValueError("This new object is not compatible with editor object class (%s)" % self.value.__class__)
        self.value = obj
        self.cells[pos] = val
        # Adding a new trait and more addable cell(s)
        traits_to_add = {}
        traitname = 'cell_%d_%d' % pos
        traitvalue = val
        if self.has_trait(traitname):
            self.set_trait(traitname, traitvalue)
        else:
            trait = self.traitclass(traitvalue)
            traits_to_add[traitname] = trait
        addable_traitname = 'add_%d_%d' % pos
        if self.has_trait(addable_traitname):
            delattr(self.__class__, addable_traitname)
            del self._trait_values[addable_traitname]
        for pos in self.adapter.addable_cells(self.value):
            emptytraitname = 'add_%d_%d' % pos
            if not self.has_trait(emptytraitname):
                emptytrait = self.traitclass(self.traitclass.default_value)
                emptytrait.name = emptytraitname
                traits_to_add[emptytraitname] = emptytrait
        #print(traits_to_add)
        self.add_traits(**traits_to_add)
        self.draw()

    def remove_cell(self, pos):
        if not hasattr(self.adapter, 'remove_cell'):
            raise TypeError("Cannot remove cell from this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.remove_cell(obj, pos)
        except:
            raise ValueError("Unable to remove cell (position=%s)" % str(pos))
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
        if not hasattr(self.adapter, 'append_row'):
            raise TypeError("Cannot append row to this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.append_row(obj, r)
        except:
            raise ValueError("Unable to append row")
        self.set_value(obj) # Will take care of everything

    def insert_row(self, index, r=None):
        if not hasattr(self.adapter, 'insert_row'):
            raise TypeError("Cannot insert row to this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.insert_row(obj, index, r)
        except:
            raise ValueError("Unable to insert row")
        self.set_value(obj) # Will take care of everything

    def remove_row(self, index=None):
        if not hasattr(self.adapter, 'remove_row'):
            raise TypeError("Cannot remove row from this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.remove_row(obj, index)
        except:
            raise ValueError("Unable to remove row")
        self.set_value(obj) # Will take care of everything

    def append_column(self, r=None):
        if not hasattr(self.adapter, 'append_column'):
            raise TypeError("Cannot append column to this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.append_column(obj, r)
        except:
            raise ValueError("Unable to append column")
        self.set_value(obj) # Will take care of everything

    def insert_column(self, index, r=None):
        if not hasattr(self.adapter, 'insert_column'):
            raise TypeError("Cannot insert column to this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.insert_column(obj, index, r)
        except:
            raise ValueError("Unable to insert column")
        self.set_value(obj) # Will take care of everything

    def remove_column(self, index=None):
        if not hasattr(self.adapter, 'remove_column'):
            raise TypeError("Cannot remove column from this object.")
        obj = copy(self.value)
        try:
            obj = self.adapter.remove_column(obj, index)
        except:
            raise ValueError("Unable to remove column")
        self.set_value(obj) # Will take care of everything

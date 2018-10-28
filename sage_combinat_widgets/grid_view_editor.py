# -*- coding: utf-8 -*-
r"""
An editable GridViewEditor for Sage Jupyter Notebook

EXAMPLES ::
    sage: from sage_combinat_widgets import GridViewEditor
    sage: t = StandardTableau([[1, 2, 5, 6], [3], [4]])
    sage: e = GridViewEditor(t)
    sage: e.addable_cells()
    [(0, 4), (1, 1), (3, 0)]
    sage: from sage.graphs.generators.basic import GridGraph
    sage: g = GridGraph((4,3))
    sage: e = GridViewEditor(g)
    sage: R = PolynomialRing(QQ, 9, 'x')
    sage: A = matrix(R, 3, 3, R.gens())
    sage: e = GridViewEditor(A)

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
from sage.misc.abstract_method import AbstractMethod

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

def get_adapter(obj):
    r"""
    Return an adapter object for Sage object `obj`.
    TESTS::
       sage: from sage_combinat_widgets.grid_view_editor import get_adapter
       sage: from sage.combinat.tableau import StandardTableaux
       sage: t = StandardTableaux(7).random_element()
       sage: ta = get_adapter(t)
       sage: ta.cellzero
       0
    """
    from sage.combinat.tableau import Tableau
    if issubclass(obj.__class__, Tableau):
        from sage.combinat.tableau import SemistandardTableau, StandardTableau
        if issubclass(obj.__class__, StandardTableau):
            from sage_widget_adapters.combinat.tableau_grid_view_adapter import StandardTableauGridViewAdapter
            return StandardTableauGridViewAdapter()
        if issubclass(obj.__class__, SemistandardTableau):
            from sage_widget_adapters.combinat.tableau_grid_view_adapter import SemistandardTableauGridViewAdapter
            return SemistandardTableauGridViewAdapter()
        from sage_widget_adapters.combinat.tableau_grid_view_adapter import TableauGridViewAdapter
        return TableauGridViewAdapter()
    from sage.matrix.matrix2 import Matrix
    if issubclass(obj.__class__, Matrix):
        from sage_widget_adapters.matrix.matrix_grid_view_adapter import MatrixGridViewAdapter
        return MatrixGridViewAdapter(obj)
    from sage.graphs.graph import Graph
    if issubclass(obj.__class__, Graph):
        from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
        return GraphGridViewAdapter()

class cdlink(traitlets.link):
    r"""
    A directional link (for a start) with type casting
    """
    def __init__(self, source, target, cast):
        r"""
        TESTS::
            sage: from sage_combinat_widgets.grid_view_editor import cdlink
            sage: from ipywidgets import Checkbox, Text
            sage: b = Checkbox()
            sage: t = Text()
            sage: l = cdlink((b, 'value'), (t, 'value'), str)
            sage: t.value
            u'False'
        """
        self.source, self.target, self.to_cell = source, target, cast
        try:
            setattr(target[0], target[1], cast(getattr(source[0], source[1])))
        finally:
            source[0].observe(self._update_target, names=source[1])
            target[0].observe(self._update_source, names=target[1])

    def _update_target(self, change):
        if self.updating:
            return
        with self._busy_updating():
            setattr(self.target[0], self.target[1], self.to_cell(change.new))

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

    def __init__(self, obj, adapter=None):
        r"""
        Initialize editor.

        INPUT:
        * a Sage object `obj`
        * an adapter object (optional)

        TESTS::

            sage: from sage_combinat_widgets import GridViewEditor
            sage: from sage.all import matrix, graphs
            sage: from sage.graphs.generic_graph import GenericGraph
            sage: g = graphs.AztecDiamondGraph(3)
            sage: e = GridViewEditor(g)
            sage: t = StandardTableaux(5).random_element()
            sage: e = GridViewEditor(t)
            sage: f = x^5
            sage: v = vector((1,2,3))
            sage: e = GridViewEditor(v)
            Traceback (most recent call last):
            ...
            TypeError: Cannot find an Adapter for this object (<type 'sage.modules.vector_integer_dense.Vector_integer_dense'>)
            sage: e = GridViewEditor(f)
            Traceback (most recent call last):
            ...
            TypeError: Is this object really grid-representable?
        """
        try:
            cells = list(obj)
        except:
            raise TypeError("Is this object really grid-representable?")
        super(GridViewEditor, self).__init__()
        self.value = obj
        if adapter:
            self.adapter = adapter
        else:
            self.adapter = get_adapter(obj)
        if not self.adapter:
            raise TypeError("Cannot find an Adapter for this object (%s)" % obj.__class__)
        self.compute()
        self.links = []

    def to_cell(self, val):
        r"""
        From a widget cell value `val`,
        return a valid editor cell value.
        Will be overloaded in widget code.
        """
        return val

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

    def modified_add_traits(self, **traits):
        r"""
        Dynamically add trait attributes to the HasTraits instance.
        Modified code according to Ryan Morshead's pull request
        Cf https://github.com/ipython/traitlets/pull/501
        """
        cls = self.__class__
        attrs = {"__module__": cls.__module__}
        if hasattr(cls, "__qualname__"):
          # __qualname__ introduced in Python 3.3 (see PEP 3155)
          attrs["__qualname__"] = cls.__qualname__
        attrs.update(traits)
        self.__class__ = type(cls.__name__, (cls,), attrs)
        for trait in traits.values():
            trait.instance_init(self)

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
        celltype = self.adapter.celltype
        traitclass = self.adapter.traitclass
        default_value = self.adapter.cellzero
        traits_to_add = {}
        for pos in self.addable_cells():
            # Empty traits for addable cells
            emptytraitname = 'add_%d_%d' % pos
            try:
                emptytrait = traitclass(default_value)
            except:
                try:
                    emptytrait = traitclass(celltype)
                except:
                    raise TypeError("Cannot init the trait (traitclass=%s, celltype=%s, default_value=%s)" % (traitclass, celltype, default_value))
            emptytrait.name = emptytraitname
            traits_to_add[emptytraitname] = emptytrait
        for pos, val in self.cells.items():
            traitname = 'cell_%d_%d' % pos
            traitvalue = val
            if traitname in self._trait_values:
                self._trait_values[traitname] = traitvalue
            else:
                try:
                    trait = traitclass(traitvalue)
                except:
                    try:
                        trait = traitclass(celltype)
                        trait.value = traitvalue
                    except:
                        raise TypeError("Cannot init the trait (traitclass=%s, celltype=%s, default_value=%s)" % (traitclass, celltype, default_value))
                trait.name = traitname
                traits_to_add[traitname] = trait
        self.traitclass = traitclass
        self.modified_add_traits(**traits_to_add)

    def reset_links(self):
        for lnk in self.links:
            lnk.unlink()
        self.links = []

    def draw(self, cast=None):
        r"""
        Build the visual representation
        and cdlink objects -- with cast function `cast`.
        """
        pass

    def get_value(self):
        return self.value

    def set_value(self, obj, compute=False):
        if not self.validate(obj):
            raise ValueError("Object %s is not compatible." % str(obj))
        self.value = obj
        if compute:
            self.compute()
            self.draw()

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
        r"""
        TESTS:
        sage: from sage_combinat_widgets import GridViewEditor
        sage: t = Tableau([[1, 2, 5, 6], [3], [4]])
        sage: e = GridViewEditor(t)
        sage: from traitlets import Bunch
        sage: change = Bunch({'name': 'cell_0_2', 'old': 5, 'new': 7, 'owner': e, 'type': 'change'})
        sage: e.set_cell(change)
        sage: e.value
        [[1, 2, 7, 6], [3], [4]]
        """
        if not change.name.startswith('cell_'):
            return
        if change.new == change.old or not change.new:
            return
        pos = extract_coordinates(change.name)
        val = change.new
        obj = copy(self.value)
        new_obj = self.adapter.set_cell(obj, pos, val)
        if new_obj == obj:
            # FIXME reverse the display change
            return
        self.set_value(new_obj)
        # Edit the cell dictionary
        self.cells[pos] = val
        # Edit the trait
        traitname = 'cell_%d_%d' % pos
        self.set_trait(traitname, val)

    def addable_cells(self):
        r"""
        List addable cells for editor value
        """
        return self.adapter.addable_cells(self.value)

    def removable_cells(self):
        r"""
        List removable cells for editor value
        """
        return self.adapter.removable_cells(self.value)

    @traitlets.observe(traitlets.All)
    def add_cell(self, change):
        r"""
        TESTS:
        sage: from sage_combinat_widgets import GridViewEditor
        sage: t = Tableau([[1, 2, 5, 6], [3], [4]])
        sage: e = GridViewEditor(t)
        sage: from traitlets import Bunch
        sage: change = Bunch({'name': 'add_1_1', 'old': 0, 'new': 8, 'owner': e, 'type': 'change'})
        sage: e.add_cell(change)
        sage: e.value
        [[1, 2, 5, 6], [3, 8], [4]]
        sage: t = StandardTableau([[1, 2, 5, 6], [3], [4]])
        sage: e = GridViewEditor(t)
        sage: e.add_cell(change)
        Cell (1, 1) with value '8' cannot be added to this object!
        sage: e.value
        [[1, 2, 5, 6], [3], [4]]
        """
        if not change.name.startswith('add_') \
           or self.to_cell(change.new) == self.adapter.cellzero:
            return
        if not hasattr(self.adapter, 'add_cell'):
            raise TypeError("Cannot add cell to this object.")
        if self.adapter.add_cell.__func__.__class__ is AbstractMethod:
            return # Method not implemented
        val = change.new
        pos = extract_coordinates(change.name)
        obj = copy(self.value)
        new_obj = self.adapter.add_cell(obj, pos, val)
        if not self.validate(new_obj):
            raise ValueError("This new object is not compatible with editor object class (%s)" % self.value.__class__)
        if new_obj == obj: # The proposed change was invalid -> stop here
            # FIXME reverse the display change
            return
        self.value = new_obj
        self.cells[pos] = val
        # Adding a new trait and more addable cell(s)
        traits_to_add = {}
        traitname = 'cell_%d_%d' % pos
        traitvalue = val
        if self.has_trait(traitname):
            self.set_trait(traitname, traitvalue)
        else:
            trait = self.traitclass(self.adapter.celltype)
            trait.value = traitvalue
            traits_to_add[traitname] = trait
        previous_addable_traitname = 'add_%d_%d' % pos
        if self.has_trait(previous_addable_traitname):
            del(self.traits()[previous_addable_traitname])
            #del self._trait_values[addable_traitname]
        for pos in self.addable_cells():
            emptytraitname = 'add_%d_%d' % pos
            if not self.has_trait(emptytraitname):
                emptytrait = self.traitclass(self.adapter.celltype)
                emptytrait.name = emptytraitname
                emptytrait.value = self.adapter.cellzero
                traits_to_add[emptytraitname] = emptytrait
        self.modified_add_traits(**traits_to_add)
        self.draw()

    @traitlets.observe(traitlets.All)
    def remove_cell(self, change):
        r"""
        TESTS:
        sage: from sage_combinat_widgets import GridViewEditor
        sage: t = Tableau([[1, 2, 5, 6], [3], [4]])
        sage: e = GridViewEditor(t)
        sage: from traitlets import Bunch
        sage: e.remove_cell(Bunch({'name': 'cell_0_3', 'old': 6, 'new': 0, 'owner': e, 'type': 'change'}))
        sage: e.value
        [[1, 2, 5], [3], [4]]
        sage: e.remove_cell(Bunch({'name': 'cell_2_0', 'old': 4, 'new': 0, 'owner': e, 'type': 'change'}))
        sage: e.value
        [[1, 2, 5], [3]]
        """
        if not change.name.startswith('cell_'):
            return
        if not hasattr(self.adapter, 'remove_cell'):
            raise TypeError("Cannot remove cell from this object.")
        if hasattr(self.adapter.remove_cell, '_optional') and self.adapter.remove_cell._optional: # Not implemented
            return
        if change.old == traitlets.Undefined: # Do nothing ar widget initializing
            return
        if change.new: # should probably compare to cellzero
            return
        pos = extract_coordinates(change.name)
        obj = copy(self.value)
        new_obj = self.adapter.remove_cell(obj, pos)
        if not self.validate(new_obj):
            raise ValueError("This new object is not compatible with editor object class (%s)" % self.value.__class__)
        if new_obj == obj: # The proposed change was invalid -> stop here
            # FIXME reverse the display change
            return
        del(self.cells[pos])
        traitname = 'cell_%d_%d' % pos
        if self.has_trait(traitname):
            del(self.traits()[traitname])
            #del(self._trait_values[traitname])
        self.value = new_obj
        self.draw()

    def append_row(self, r=None):
        if not hasattr(self.adapter, 'append_row'):
            raise TypeError("Cannot append row to this object.")
        obj = copy(self.value)
        obj = self.adapter.append_row(obj, r)
        self.set_value(obj, True) # Will take care of everything

    def insert_row(self, index, r=None):
        if not hasattr(self.adapter, 'insert_row'):
            raise TypeError("Cannot insert row to this object.")
        obj = copy(self.value)
        obj = self.adapter.insert_row(obj, index, r)
        self.set_value(obj, True) # Will take care of everything

    def remove_row(self, index=None):
        if not hasattr(self.adapter, 'remove_row'):
            raise TypeError("Cannot remove row from this object.")
        obj = copy(self.value)
        obj = self.adapter.remove_row(obj, index)
        self.set_value(obj, True) # Will take care of everything

    def append_column(self, c=None):
        if not hasattr(self.adapter, 'append_column'):
            raise TypeError("Cannot append column to this object.")
        obj = copy(self.value)
        obj = self.adapter.append_column(obj, c)
        self.set_value(obj, True) # Will take care of everything

    def insert_column(self, index, c=None):
        if not hasattr(self.adapter, 'insert_column'):
            raise TypeError("Cannot insert column to this object.")
        obj = copy(self.value)
        obj = self.adapter.insert_column(obj, index, c)
        self.set_value(obj, True) # Will take care of everything

    def remove_column(self, index=None):
        if not hasattr(self.adapter, 'remove_column'):
            raise TypeError("Cannot remove column from this object.")
        obj = copy(self.value)
        obj = self.adapter.remove_column(obj, index)
        self.set_value(obj, True) # Will take care of everything

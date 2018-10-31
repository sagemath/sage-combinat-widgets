# -*- coding: utf-8 -*-
r"""
An editable GeometricViewEditor for Sage Jupyter Notebook

EXAMPLES ::
    sage: from sage.plot.plot3d.platonic import dodecahedron
    sage: from sage_combinat_widgets import GeometricViewEditor
    sage: S = dodecahedron()
    sage: e = GeometricViewEditor(S)

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
import re, traitlets
from six import add_metaclass
from copy import copy
from sage.misc.bindable_class import BindableClass
from sage.all import SageObject
from sage.structure.list_clone import ClonableList
from sage.misc.abstract_method import AbstractMethod

def extract_position(s):
    r"""
    TESTS::
        sage: from sage_combinat_widgets.geometric_view_editor import extract_position
        sage: extract_position('vert_4')
        4
    """
    patt = re.compile('_([0-9]+)')
    m = patt.search(s)
    if m:
        return int(m.groups()[0])

def get_adapter(obj):
    r"""
    Return an adapter object for Sage object `obj`.
    TESTS::
       sage: from sage_combinat_widgets.geometric_view_editor import get_adapter
       sage: from sage.plot.plot3d.platonic import dodecahedron
       sage: S = dodecahedron()
       sage: Sa = get_adapter(S)
       sage: Sa.objclass
       <type 'sage.plot.plot3d.index_face_set.IndexFaceSet'>
    """
    from sage.plot.plot3d.index_face_set import IndexFaceSet
    if issubclass(obj.__class__, IndexFaceSet):
        from sage_widget_adapters.geometry.polyhedron_geometric_view_adapter import PolyhedronGeometricViewAdapter
        return PolyhedronGeometricViewAdapter()

class cdlink(traitlets.link):
    r"""
    A directional link (for a start) with type casting
    """
    def __init__(self, source, target, cast):
        r"""
        TESTS::
            sage: from sage_combinat_widgets.geometric_view_editor import cdlink
            sage: from ipywidgets import Checkbox, Text
            sage: b = Checkbox()
            sage: t = Text()
            sage: l = cdlink((b, 'value'), (t, 'value'), str)
            sage: t.value
            u'False'
        """
        self.source, self.target, self.to_vertex = source, target, cast
        try:
            setattr(target[0], target[1], cast(getattr(source[0], source[1])))
        finally:
            source[0].observe(self._update_target, names=source[1])
            target[0].observe(self._update_source, names=target[1])

    def _update_target(self, change):
        if self.updating:
            return
        with self._busy_updating():
            setattr(self.target[0], self.target[1], self.to_vertex(change.new))

import sage.misc.classcall_metaclass
class MetaHasTraitsClasscallMetaclass(traitlets.MetaHasTraits, sage.misc.classcall_metaclass.ClasscallMetaclass):
    pass
@add_metaclass(MetaHasTraitsClasscallMetaclass)
class BindableClassWithMeta(BindableClass):
    pass
class BindableEditorClass(traitlets.HasTraits, BindableClassWithMeta):
    pass

class GeometricViewEditor(BindableEditorClass):
    r"""Base Editor for geometric-representable Sage Objects

    Composed of vertices. No decision made here about vertex representation.
    The vertex trait objects will store values
    that are refered to through object vertices as a dictionary
    with positions (integers) as keys
    """

    def __init__(self, obj, adapter=None):
        r"""
        Initialize editor.

        INPUT:
        * a Sage object `obj`
        * an adapter object (optional)

        TESTS::

            sage: from sage_combinat_widgets import GeometricViewEditor
            sage: S = dodecahedron()
            sage: e = GeometricViewEditor(S)
        """
        super(GeometricViewEditor, self).__init__()
        self.value = obj
        if adapter:
            self.adapter = adapter
        else:
            self.adapter = get_adapter(obj)
        if not self.adapter:
            raise TypeError("Cannot find an Adapter for this object (%s)" % obj.__class__)
        self.compute()
        #self.links = []

    def to_vertex(self, val):
        r"""
        From a widget vertex value `val`,
        return a valid editor vertex value.
        Will be overloaded in widget code.
        """
        return val

    def validate(self, obj, value=None, obj_class=None):
        r"""
        Validate the object type
        """
        if obj_class:
            return issubclass(obj.__class__, obj_class)
        return issubclass(obj.__class__, self.adapter.objclass)

    def compute(self, obj=None):
        if not obj:
            obj = self.value
        if not obj:
            return
        try:
            self.vertices = self.adapter.compute_vertices(obj)
        except:
            print("Cannot compute vertices for this object")
            self.vertices = {}

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

    def get_vertices(self):
        return self.vertices

    def set_value_from_vertices(self, obj_class=None, vertices={}):
        r"""We have an object value, but we want to change it according to vertices
        Yet we want to keep the same class (or warn if that's impossible)
        INPUT::
        * an object class (by default: self.value.__class__)
        * a vertices dictionary (i,j)->val
        """
        if not obj_class and self.value:
            obj_class = self.value.__class__
        if not obj_class:
            return
        if hasattr(self.adapter, 'from_vertices'):
            try:
                obj = self.adapter.from_vertices(vertices)
            except:
                raise ValueError("Could not make an object of class '%s' from given vertices" % str(obj_class))
        elif hasattr(obj_class, 'vertices') or hasattr(obj_class, 'rows'): # e.g. a tableau / matrix / vector
            positions = sorted(list(vertices.keys()))
            for cl in obj_class.__mro__:
                try:
                    obj = cl([[vertices[pos] for pos in positions if pos[0]==i] for i in uniq([t[0] for t in positions])])
                except:
                    print("These vertices cannot be turned into a %s" % cl)
        else:
            raise TypeError("Unable to cast the given vertices into a geometric-like object.")
        if not self.validate(obj, None, obj_class):
            raise ValueError("Could not make a compatible ('%s')  object from given vertices" % str(obj_class))
        self.set_value(obj)

    def set_vertex(self, change):
        r"""
        TESTS:
        sage: from sage_combinat_widgets import GeometricViewEditor
        sage: from sage.plot.plot3d.platonic import dodecahedron
        sage: S = dodecahedron()
        sage: e = GeometricViewEditor(S)
        sage: from traitlets import Bunch
        sage: change = Bunch({'name': 'vert_1', 'old': (0,0,1), 'new': (0,0,2), 'owner': e, 'type': 'change'})
        sage: e.set_vertex(change)
        sage: e.value.vertex_list()[0]
        (0.0, 0.0, 2.0)
        """
        if not change.name.startswith('vert_'):
            return
        if change.new == change.old or not change.new:
            return
        pos = extract_position(change.name)
        obj = copy(self.value)
        new_obj = self.adapter.set_vertex(obj, pos, change.new)
        if new_obj == obj:
            # FIXME reverse the display change
            return
        self.set_value(new_obj)
        # Edit the vertex dictionary
        self.vertices[pos] = change.new
        # Edit the trait
        traitname = 'vertex_%d' % pos
        #self.set_trait(traitname, change.new)

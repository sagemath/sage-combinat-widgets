# -*- coding: utf-8 -*-
r"""
Grid View Adapter for polyhedra

**Grid View polyhedron operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |



AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
import traitlets
from sage.plot.plot3d.index_face_set import IndexFaceSet
from sage.plot.plot3d.platonic import *
from sage.graphs.digraph import DiGraph
from sage_widget_adapters.generic_geometric_view_adapter import GeometricViewAdapter
from copy import copy

class PolyhedronGeometricViewAdapter(GeometricViewAdapter):
    objclass = IndexFaceSet
    traitclass = traitlets.Tuple

    def compute_vertices(self, obj):
        ret = {}
        i = 0
        for v in obj.vertices():
            ret[i] = v
            i += 1
        return ret

    def set_vertex(self, obj, pos, pt):
        verts = obj.vertices()
        new_verts = []
        i = 0
        for v in obj.vertices():
            if i == pos:
                new_verts.append(pt)
            else:
                new_verts.append(v)
            i += 1
        return self.objclass(new_verts)


# -*- coding: utf-8 -*-
r"""
Grid View Adapter for grid-representable graphs

**Grid View graphs operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~GraphGridViewAdapter.cell_to_display` | Static method for typecasting cell content to widget display value
    :meth:`~GraphGridViewAdapter.display_to_cell` | Instance method for typecasting widget display value to cell content
    :meth:`~GraphGridViewAdapter.compute_cells` | Compute graph cells as a dictionary { coordinate pair : label }
    :meth:`~GraphGridViewAdapter.from_cells` | Create a new graph from a cells dictionary
    :meth:`~GraphGridViewAdapter.get_cell` | Get the graph cell content (i.e. None)
    :meth:`~GraphGridViewAdapter.addable_cells` | List addable cells
    :meth:`~GraphGridViewAdapter.removable_cells` | List removable cells
    :meth:`~GraphGridViewAdapter.add_cell` | Add a cell
    :meth:`~GraphGridViewAdapter.remove_cell` | Remove a cell
    :meth:`~GraphGridViewAdapter.append_row` | Append a row
    :meth:`~GraphGridViewAdapter.remove_row` | Remove a row at given index
    :meth:`~GraphGridViewAdapter.append_column` | Append a column
    :meth:`~GraphGridViewAdapter.remove_column` | Remove a column at given index

AUTHORS ::

    Odile Bénassy, Nicolas Thiéry

"""
from sage.graphs.graph import Graph
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter
from six import text_type

class GraphGridViewAdapter(GridViewAdapter):
    r"""
    Grid view adapter for grid-representable graphs.

    ATTRIBUTES::
        * ``objclass`` -- Graph
        * ``celltype`` -- bool
        * ``cellzero`` -- False
    """
    objclass = Graph
    celltype = bool
    cellzero = False

    @staticmethod
    def cell_to_display(cell_content, display_type=bool):
        r"""
        From object cell content
        to widget display value.

        TESTS ::

            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: GraphGridViewAdapter.cell_to_display(True)
            True
            sage: from six import text_type
            sage: GraphGridViewAdapter.cell_to_display("my string", text_type)
            ''
        """
        if display_type == text_type:
            return ''
        elif cell_content:
            return cell_content
        elif display_type == bool:
            return False

    def display_to_cell(self, display_value, display_type=bool):
        r"""
        From widget cell value
        to object display content

        TESTS ::

            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: ga = GraphGridViewAdapter()
            sage: ga.display_to_cell(True)
            True
            sage: ga.display_to_cell('')
            False
        """
        if not display_value or display_type == text_type:
            return self.cellzero
        return display_value

    @staticmethod
    def compute_cells(obj):
        r"""
        From the graph vertices,
        make a dictionary { coordinates pair : None }

        TESTS ::

            sage: from sage.graphs.generators.families import AztecDiamondGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = AztecDiamondGraph(2)
            sage: GraphGridViewAdapter.compute_cells(g)
            {(0, 1): None,
            (0, 2): None,
            (1, 0): None,
            (1, 1): None,
            (1, 2): None,
            (1, 3): None,
            (2, 0): None,
            (2, 1): None,
            (2, 2): None,
            (2, 3): None,
            (3, 1): None,
            (3, 2): None}
        """
        cells = {}
        for v in obj.vertices():
            cells[v] = None
        return cells

    @classmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : None }
        return a graph with one vertex for every coordinates pair

        TESTS ::

            sage: from sage.graphs.generators.families import AztecDiamondGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: GraphGridViewAdapter.from_cells({(0, 0): None, (0, 1): None, (1, 0): None, (1, 1): None, (2, 0): None, (2, 1): None})
            Graph on 6 vertices
        """
        g = Graph()
        g.add_vertices(list(cells.keys()))
        return cls.objclass(g)

    @staticmethod
    def get_cell(obj, pos):
        r"""
        From a graph `graph` and a tuple `pos`,
        return the object cell value at position `pos`.

        TESTS ::

            sage: from sage.graphs.generators.families import AztecDiamondGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = AztecDiamondGraph(2)
            sage: GraphGridViewAdapter.get_cell(g, (1,3)) is None
            True
        """
        return None

    @staticmethod
    def addable_cells(obj):
        r"""
        No cell should be added in isolation
        except for linear graphs

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((2,3))
            sage: GraphGridViewAdapter.addable_cells(g)
            []
            sage: g = GridGraph((1,3))
            sage: GraphGridViewAdapter.addable_cells(g)
            [(0, 3)]
        """
        if not obj.num_verts():
            return [(0,0)]
        row_max, col_max = 0, 0
        for t in obj.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
            if row_max > 0 and col_max > 0:
                return []
        if row_max > 0:
            return [(row_max + 1, 0)]
        elif col_max > 0:
            return [(0, col_max + 1)]
        return [(0,1),(1,0)]

    @staticmethod
    def removable_cells(obj):
        r"""
        No cell should be removed in isolation
        except for linear graphs

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((2,3))
            sage: GraphGridViewAdapter.removable_cells(g)
            []
            sage: g = GridGraph((1,3))
            sage: GraphGridViewAdapter.removable_cells(g)
            [(0, 2)]
        """
        row_max, col_max = 0, 0
        for t in obj.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
            if row_max > 0 and col_max > 0:
                return []
        if row_max > 0:
            return [(row_max, 0)]
        elif col_max > 0:
            return [(0, col_max)]
        return [(0,0)]

    def add_cell(self, obj, pos, val=None, dirty={}):
        r"""
        Add a cell to the graph.

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((1,2))
            sage: ga = GraphGridViewAdapter()
            sage: ga.add_cell(g, (0,2))
            Grid Graph for [1, 2]: Graph on 3 vertices
        """
        if not pos in self.addable_cells(obj):
            raise ValueError("Position '%s' is not addable." % str(pos))
        if pos in obj.vertices():
            raise ValueError("This cell (position=%s) is already in the graph." % str(pos))
        obj.add_vertex(pos)
        return obj

    def remove_cell(self, obj, pos, dirty={}):
        r"""
        Remove a cell from the graph.

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((1, 2))
            sage: ga = GraphGridViewAdapter()
            sage: ga.remove_cell(g, (0,1))
            Grid Graph for [1, 2]: Graph on 1 vertex
        """
        if not pos in self.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))
        obj.delete_vertex(pos)
        return obj

    def append_row(self, obj):
        r"""
        Add a row to the graph.

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((3,2))
            sage: ga = GraphGridViewAdapter()
            sage: ga.append_row(g)
            Grid Graph for [3, 2]: Graph on 8 vertices
        """
        row_max, col_max = 0, 0
        for t in obj.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        obj.add_vertices([(row_max + 1, j) for j in range(col_max + 1)])
        return obj

    def remove_row(self, obj, index=None):
        r"""
        Remove a row from the graph

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((3,2))
            sage: ga = GraphGridViewAdapter()
            sage: ga.remove_row(g)
            Grid Graph for [3, 2]: Graph on 4 vertices
        """
        row_max, col_max = 0, 0
        for t in obj.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        obj.delete_vertices([(row_max, j) for j in range(col_max + 1)])
        return obj

    def append_column(self, obj):
        r"""
        Add a column to the graph.

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((3,2))
            sage: ga = GraphGridViewAdapter()
            sage: ga.append_column(g)
            Grid Graph for [3, 2]: Graph on 9 vertices
        """
        row_max, col_max = 0, 0
        for t in obj.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        obj.add_vertices([(i, col_max + 1) for i in range(row_max + 1)])
        return obj

    def remove_column(self, obj, index=None):
        r"""
        Remove a column from the graph

        TESTS ::

            sage: from sage.graphs.generators.basic import GridGraph
            sage: from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
            sage: g = GridGraph((3,2))
            sage: ga = GraphGridViewAdapter()
            sage: ga.remove_column(g)
            Grid Graph for [3, 2]: Graph on 3 vertices
        """
        row_max, col_max = 0, 0
        for t in obj.vertex_iterator():
            row_max = max(row_max, t[0])
            col_max = max(col_max, t[1])
        obj.delete_vertices([(i, col_max) for i in range(row_max + 1)])
        return obj

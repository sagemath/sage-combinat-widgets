from .grid_view_editor import GridViewEditor
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML
from sage.misc.misc import uniq
import traitlets

cell_layout = Layout(width='3em',height='2em', margin='0',padding='0')
blank_layout = Layout(width='3em',height='2em', margin='0', border='0')
css_lines = []
css = HTML("<style>%s</style>" % '\n'.join(css_lines))

try:
    ip = get_ipython()
    for base in ip.__class__.__mro__:
        """If we are in a notebook, we will find 'notebook' in those names"""
        if 'otebook' in base.__name__:
            ip.display_formatter.format(css)
            break
except:
    pass # We are in the test environment


class BlankCell(Text):
    r"""A blank placeholder cell

    TESTS::
        sage: from sage_combinat_widgets import BlankCell
        sage: b = BlankCell()
    """

    def __init__(self):
        super(BlankCell, self).__init__('', disabled=True)
        self.layout = blank_layout
        self.add_class('blankcell')

    def reset(self):
        pass


def compute_tooltip(t):
    r"""From a tuple (i,j),
    we just want the string 'i,j'
    """
    return str(t)[-1:1]

class GridViewWidget(GridViewEditor, VBox):
    r"""A widget for all grid-representable Sage objects
    """

    def __init__(self, obj, cell_classes=[Text], blank_class=BlankCell):
        r"""
        TESTS::

            sage: from sage_combinat_widgets import *
            sage: t = StandardTableaux(15).random_element()
            sage: ta = TableauGridViewAdapter(t.parent(), t)
            sage: w = GridViewWidget(ta)
            sage: from sage.graphs.generators.families import AztecDiamondGraph
            sage: az = AztecDiamondGraph(4)
            sage: aza = GraphGridViewAdapter(az)
            sage: w = GridViewWidget(aza)
        """
        GridViewEditor.__init__(self, obj)
        VBox.__init__(self)
        self._model_id = list(self.get_manager_state()['state'].keys())[-1] # For some reason, it lost its _model_id
        self.compute()
        positions = sorted(list(self.cells.keys()))
        rows = [[(pos, self.cells[pos]) for pos in positions if pos[0]==i] for i in uniq([t[0] for t in positions])]
        vbox_children = []
        def cell_class_index(pos):
            # Such function can enable for example various shapes or colors
            return 0
        for i in range(len(rows)):
            j = 0
            hbox_children = []
            while j<=max([t[0][1] for t in rows[i]]):
                if (i,j) in positions:
                    cell_content = self.cells[(i,j)]
                    cell_class = cell_classes[cell_class_index((i,j))]
                    if cell_content is None:
                        cell_string = ''
                    else:
                        cell_string = str(cell_content)
                    cell = cell_class(cell_string, placeholder=cell_string, tooltip=compute_tooltip((i,j)), layout=cell_layout)
                    # TODO write some typecasting (possibly requires subclassing cell_class or traitlets.link)
                    # traitlets.link((self, 'cell_%d_%d' % (i,j)), (cell, 'value'))
                    cell.add_class('gridcell')
                    hbox_children.append(cell)
                else:
                    hbox_children.append(blank_class())
                j+=1
            vbox_children.append(HBox(hbox_children))
        self.children = vbox_children

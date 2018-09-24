from .grid_view_editor import GridViewEditor
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML
from sage.misc.misc import uniq
import traitlets

cell_layout = Layout(width='3em',height='2em', margin='0',padding='0')
blank_layout = Layout(width='3em',height='2em', margin='0', border='0')
addable_layout = Layout(width='3em',height='2em', margin='0', border='0')
css_lines = []
css_lines.append(".widget-text INPUT { border-collapse: collapse !important }")
css_lines.append(".blankcell INPUT {border:0px !important}")
css_lines.append(".addablecell INPUT {border:1px dashed #999 !important}")
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

class AddableCell(Text):
    r"""An addable placeholder for adding a cell to the widget

    TESTS::
        sage: from sage_combinat_widgets import AddableCell
        sage: a = AddableCell()
    """

    def __init__(self, position):
        super(AddableCell, self).__init__('')
        self.layout = addable_layout
        self.add_class('addablecell')
        self.position = position

def compute_tooltip(t):
    r"""From a tuple (i,j),
    we just want the string 'i,j'
    """
    return str(t)[-1:1]

class GridViewWidget(GridViewEditor, VBox):
    r"""A widget for all grid-representable Sage objects
    """

    def __init__(self, obj, cell_widget_classes=[Text], blank_widget_class=BlankCell, addable_widget_class=AddableCell):
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
        self.cell_widget_classes = cell_widget_classes
        self.blank_widget_class = blank_widget_class
        self.addable_widget_class = addable_widget_class
        self.compute()
        self.draw()

    def draw(self):
        r"""
        Add children to the Box:
        * Sage object/gris editor cells
        * Blank cells for empty cells in a row
        * Addable cells if any
        """
        positions = sorted(list(self.cells.keys()))
        rows = [[(pos, self.cells[pos]) for pos in positions if pos[0]==i] \
                for i in uniq([t[0] for t in positions])]
        vbox_children = []
        def cell_widget_class_index(pos):
            # Such function can enable for example various shapes or colors
            return 0
        addable_positions = []
        if self.addable_widget_class and hasattr(self, 'addable_cells'):
            addable_positions = sorted(list(self.addable_cells()))
            addable_rows = [(i,[pos for pos in addable_positions if pos[0]==i]) \
                            for i in uniq([t[0] for t in addable_positions])]
        for i in range(len(rows)):
            j = 0
            hbox_children = []
            while j<=max([t[0][1] for t in rows[i]]):
                if (i,j) in positions:
                    cell_content = self.cells[(i,j)]
                    cell_widget_class = self.cell_widget_classes[cell_widget_class_index((i,j))]
                    if cell_content is None:
                        cell_string = ''
                    else:
                        cell_string = str(cell_content)
                    cell = cell_widget_class(cell_string,
                                             placeholder=cell_string,
                                             tooltip=compute_tooltip((i,j)), # For buttons, menus ..
                                             layout=cell_layout)
                    cell.position = (i,j)
                    # TODO write some typecasting (possibly requires subclassing traitlets.link)
                    # traitlets.mylink((self, 'cell_%d_%d' % (i,j)), (cell, 'value'))
                    cell.add_class('gridcell')
                    hbox_children.append(cell)
                elif (i,j) in addable_positions:
                    hbox_children.append(self.addable_widget_class((i,j)))
                else:
                    hbox_children.append(self.blank_widget_class())
                j+=1
                if (i,j) in addable_positions:
                    hbox_children.append(self.addable_widget_class((i,j)))
            vbox_children.append(HBox(hbox_children))
        for row in addable_rows:
            if row[0] > i:
                vbox_children.append(HBox([self.addable_widget_class((i,j)) for c in row[1]]))
        self.children = vbox_children

from .grid_view_editor import *
from sage.graphs.generic_graph import GenericGraph
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML, Button
from sage.misc.misc import uniq
from traitlets import observe

textcell_layout = Layout(width='3em',height='2em', margin='0', padding='0')
textcell_wider_layout = Layout(width='7em',height='3em', margin='0', padding='0')
buttoncell_layout = Layout(width='5em',height='4em', margin='0', padding='0')
css_lines = []
css_lines.append(".widget-text INPUT { border-collapse: collapse !important}")
css_lines.append(".gridbutton {border:1px solid #999}")
css_lines.append(".blankbutton {border:0px !important; background-color: white}")
css_lines.append(".blankcell INPUT {border:0px !important}")
css_lines.append(".addablecell INPUT, .removablecell INPUT {background-position: right top; background-size: 1em; background-repeat: no-repeat}")
css_lines.append(".addablecell INPUT {border:1px dashed #999 !important; background-image: url('Plus.png')}")
css_lines.append(".removablecell INPUT {background-image: url('Minus.png')}")
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

class TextCell(Text):
    r"""A regular text grid cell

    TESTS::
        sage: from sage_combinat_widgets.grid_view_widget import TextCell
        sage: b = TextCell('my text', (1,2))
    """

    def __init__(self, content, position, layout=textcell_layout, **kws):
        super(TextCell, self).__init__(content, layout=layout, continuous_update=False, **kws)
        self.position = position
        self.add_class('gridcell')

class WiderTextCell(Text):
    r"""A regular text grid cell

    TESTS::
        sage: from sage_combinat_widgets.grid_view_widget import WiderTextCell
        sage: b = WiderTextCell('my text', (1,2))
    """

    def __init__(self, content, position, layout=textcell_wider_layout, **kws):
        super(WiderTextCell, self).__init__(content, layout=layout, continuous_update=False, **kws)
        self.position = position
        self.add_class('gridcell')

class ButtonCell(Button):
    r"""A button grid cell

    TESTS::
        sage: from sage_combinat_widgets.grid_view_widget import ButtonCell
        sage: b = ButtonCell('None', (1,2))
    """

    def __init__(self, content, position, layout=buttoncell_layout, **kws):
        super(ButtonCell, self).__init__(layout=layout, **kws)
        self.position = position
        self.add_class('gridbutton')

class BlankCell(Text):
    r"""A blank placeholder cell

    TESTS::
        sage: from sage_combinat_widgets.grid_view_widget import BlankCell
        sage: b = BlankCell()
    """

    def __init__(self, layout=textcell_layout):
        super(BlankCell, self).__init__('', layout=layout, disabled=True)
        self.add_class('blankcell')

class BlankButton(Button):
    r"""A blank placeholder button

    TESTS::
        sage: from sage_combinat_widgets.grid_view_widget import BlankButton
        sage: b = BlankButton()
    """

    def __init__(self, layout=buttoncell_layout):
        super(BlankButton, self).__init__(layout=layout, disabled=True)
        self.add_class('blankbutton')

class AddableCell(Text):
    r"""An addable placeholder for adding a cell to the widget

    TESTS::
        sage: from sage_combinat_widgets.grid_view_widget import AddableCell
        sage: a = AddableCell((3,4))
    """

    def __init__(self, position, layout=textcell_layout):
        super(AddableCell, self).__init__('', layout=layout, continuous_update=False)
        self.position = position
        self.add_class('addablecell')

def compute_tooltip(t):
    r"""From a tuple (i,j),
    we just want the string 'i,j'
    """
    return str(t)[-1:1]

def get_model_id(w):
    r"""
    For some reason, our widgets seem to lose their model_id
    This *hack* recovers it
    """
    for u in w.widgets:
        if w.widgets[u] == w:
            return u

class GridViewWidget(GridViewEditor, VBox):
    r"""A widget for all grid-representable Sage objects
    """

    def __init__(self, obj, cell_layout=None, cell_widget_classes=[TextCell], blank_widget_class=BlankCell, addable_widget_class=AddableCell):
        r"""
        TESTS::

            sage: from sage_combinat_widgets.grid_view_widget import *
            sage: t = StandardTableaux(15).random_element()
            sage: w = GridViewWidget(t)
            sage: from sage.graphs.generators.families import AztecDiamondGraph
            sage: az = AztecDiamondGraph(4)
            sage: w = GridViewWidget(az, cell_widget_classes=[ButtonCell], blank_widget_class=BlankButton)
        """
        GridViewEditor.__init__(self, obj)
        VBox.__init__(self)
        self._model_id = get_model_id(self)
        if not cell_layout:
            if issubclass(self.value.__class__, GenericGraph): # i.e. a graph
                cell_layout = buttoncell_layout
                cast = self.adapter.bool_to_cell
            else:
                cell_layout = textcell_layout
                cast = self.adapter.unicode_to_cell
        self.cell_layout = cell_layout
        self.cell_widget_classes = cell_widget_classes
        self.blank_widget_class = blank_widget_class
        self.addable_widget_class = addable_widget_class
        self.cast = cast
        self.draw()

    def to_cell(self, val):
        r"""
        From a widget cell value `val`,
        return a valid editor cell value.
        TESTS::
            sage: from sage_combinat_widgets.grid_view_widget import GridViewWidget
            sage: t = StandardTableaux(5).random_element()
            sage: w = GridViewWidget(t)
            sage: w.to_cell('3')
            3
        """
        return self.cast(val)

    def add_links(self):
        r"""
        Link each individual widget cell
        to its corresponding trait in the editor
        """
        for pos in self.cells.keys():
            traitname = 'cell_%d_%d' % (pos)
            try:
                child = self.children[pos[0]].children[pos[1]]
            except:
                child = None
            if child and hasattr(child, 'value') and traitname in self.traits():
                self.links.append(cdlink((child, 'value'), (self, traitname), self.cast))
        for pos in self.addable_cells():
            # A directional link to trait 'add_i_j'
            traitname = 'add_%d_%d' % (pos)
            try:
                child = self.children[pos[0]].children[pos[1]]
                if child and hasattr(child, 'value') and traitname in self.traits():
                    self.links.append(cdlink((child, 'value'), (self, traitname), self.cast))
            except:
                pass

    def draw(self):
        r"""
        Add children to the Box:
        * Sage object/gris editor cells
        * Blank cells for empty cells in a row
        * Addable cells if any
        """
        self.reset_links()
        positions = sorted(list(self.cells.keys()))
        rows = [[(pos, self.cells[pos]) for pos in positions if pos[0]==i] \
                for i in uniq([t[0] for t in positions])]
        vbox_children = []
        def cell_widget_class_index(pos):
            # Such function can enable for example various shapes or colors
            return 0
        addable_positions = self.addable_cells()
        addable_rows = []
        removable_positions = self.removable_cells()
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
                        cell_string = self.adapter.cell_to_unicode(cell_content)
                    cell = cell_widget_class(cell_string,
                                             (i,j),
                                             self.cell_layout,
                                             placeholder=cell_string,
                                             tooltip=compute_tooltip((i,j)) # For buttons, menus ..
                    )
                    if (i,j) in removable_positions:
                        cell.add_class('removablecell')
                    hbox_children.append(cell)
                elif (i,j) in addable_positions:
                    hbox_children.append(self.addable_widget_class((i,j), self.cell_layout))
                else:
                    hbox_children.append(self.blank_widget_class(self.cell_layout))
                j+=1
                if (i,j) in addable_positions:
                    hbox_children.append(self.addable_widget_class((i,j), self.cell_layout))
            vbox_children.append(HBox(hbox_children))
        for row in addable_rows:
            if row[0] > i:
                vbox_children.append(HBox([self.addable_widget_class((i,j), self.cell_layout) for c in row[1]]))
        self.children = vbox_children
        self.add_links()

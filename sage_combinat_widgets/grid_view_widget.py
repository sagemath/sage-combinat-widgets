from .grid_view_editor import GridViewEditor
from sage.graphs.generic_graph import GenericGraph
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML, Button
from sage.misc.misc import uniq
from traitlets import observe, link

textcell_layout = Layout(width='3em',height='2em', margin='0',padding='0')
buttoncell_layout = Layout(width='5em',height='4em', margin='0')
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


class cdlink(link):
    r"""
    A directional link (for a start) with type casting
    """
    def __init__(self, source, target, cast):
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

class TextCell(Text):
    r"""A regular text grid cell

    TESTS::
        sage: from sage_combinat_widgets import TextCell
        sage: b = TextCell()
    """

    def __init__(self, content, position, layout=textcell_layout, **kws):
        super(TextCell, self).__init__(content, layout=layout, continuous_update=False, **kws)
        self.position = position
        self.add_class('gridcell')

class ButtonCell(Button):
    r"""A button grid cell

    TESTS::
        sage: from sage_combinat_widgets import ButtonCell
        sage: b = ButtonCell()
    """

    def __init__(self, content, position, layout=buttoncell_layout, **kws):
        super(ButtonCell, self).__init__(layout=layout, **kws)
        self.position = position
        self.add_class('gridcell')

class BlankCell(Text):
    r"""A blank placeholder cell

    TESTS::
        sage: from sage_combinat_widgets import BlankCell
        sage: b = BlankCell()
    """

    def __init__(self, layout=textcell_layout):
        super(BlankCell, self).__init__('', layout=layout, disabled=True)
        self.add_class('blankcell')

class AddableCell(Text):
    r"""An addable placeholder for adding a cell to the widget

    TESTS::
        sage: from sage_combinat_widgets import AddableCell
        sage: a = AddableCell()
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

class GridViewWidget(GridViewEditor, VBox):
    r"""A widget for all grid-representable Sage objects
    """

    def __init__(self, obj, cell_layout=None, cell_widget_classes=[TextCell], blank_widget_class=BlankCell, addable_widget_class=AddableCell):
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
        if not cell_layout:
            if issubclass(self.value.__class__, GenericGraph): # i.e. a graph
                cell_layout = buttoncell_layout
                cast = self.value.bool_to_cell
            else:
                cell_layout = textcell_layout
                cast = self.value.unicode_to_cell
        self.cell_layout = cell_layout
        self.cell_widget_classes = cell_widget_classes
        self.blank_widget_class = blank_widget_class
        self.addable_widget_class = addable_widget_class
        self.compute()
        self.draw()
        self.add_links(cast)

    def add_links(self, cast):
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
                cdlink((child, 'value'), (self, traitname), cast)
        for pos in self.addable_cells():
            # A directional link to trait 'add_i_j'
            traitname = 'add_%d_%d' % (pos)
            try:
                child = self.children[pos[0]].children[pos[1]]
                if child and hasattr(child, 'value') and traitname in self.traits():
                    cdlink((child, 'value'), (self, traitname), cast)
            except:
                pass

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
        addable_rows = []
        if self.addable_widget_class and self.addable_cells():
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
                        cell_string = self.value.cell_to_unicode(cell_content)
                    cell = cell_widget_class(cell_string,
                                             (i,j),
                                             self.cell_layout,
                                             placeholder=cell_string,
                                             tooltip=compute_tooltip((i,j)) # For buttons, menus ..
                    )
                    # TODO write some typecasting (possibly requires subclassing traitlets.link)
                    # traitlets.mylink((self, 'cell_%d_%d' % (i,j)), (cell, 'value'))
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

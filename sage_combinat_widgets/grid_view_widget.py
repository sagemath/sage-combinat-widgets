from .grid_view_editor import GridViewEditor
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML
from sage.misc.misc import uniq
import traitlets

cell_layout = Layout(width='3em',height='2em', margin='0',padding='0')
blank_layout = Layout(width='3em',height='2em', margin='0', border='0')
css_lines = []
css_lines.append(".invisible {display: none; width: 0; height: 0;}")
css_lines.append(".visible {display: table}")
css_lines.append(".blankcell { background-color: white; }")
css_lines.append(".dwbutton { border-collapse: collapse; color: red; border: 1px solid #666;}")
css_lines.append(".left { border-right: 1px dotted #999; }")
css_lines.append(".right { border-left: 1px dotted #999; }")
css_lines.append(".bottom { border-top: 1px dotted #999; }")
css_lines.append(".top { border-bottom: 1px dotted #999; }")
css_lines.append(".green { background-color: lightgreen; }")
css_lines.append(".blue { background-color: lightblue; }")
css_lines.append(".pink { background-color: lightpink; }")
css_lines.append(".yellow { background-color: lightyellow; }")
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
        super(BlankCell, self).__init__(False, disabled=True)
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

    def __init__(self, obj, cell_class=Text, blank_class=BlankCell):
        r"""
        TESTS::

            sage: from sage_combinat_widgets import GridViewWidget
            sage: S = StandardTableaux(15).random_element()
            sage: w = GridViewWidget(t)
        """
        GridViewEditor.__init__(self, obj)
        VBox.__init__(self)
        positions = list(self.cells.keys())
        positions.sort()
        rows = [[(pos, self.cells[pos]) for pos in positions if pos[0]==i] for i in uniq([t[0] for t in positions])]
        vbox_children = []
        for i in range(len(rows)):
            j = 0
            hbox_children = []
            while j<len(rows[i]):
                if (i,j) in positions:
                    cell_content = self.cells[(i,j)]
                    if cell_content is None:
                        cell_string = ''
                    else:
                        cell_string = str(cell_content)
                    cell = cell_class(cell_string, placeholder=cell_string, tooltip=compute_tooltip((i,j)))
                    # TODO write some typecasting (possibly a subclass for cell_class or traitlets.link)
                    # traitlets.link((self, 'cell_%d_%d' % (i,j)), (cell, 'value'))
                    hbox_children.append(cell)
                else:
                    hbox_children.append(blank_class())
                j+=1
            vbox_children.append(HBox(hbox_children))
        self.children = vbox_children

# -*- coding: utf-8 -*-
r"""
An editable Young Tableau for Sage Jupyter Notebook

EXAMPLES ::
S = StandardTableaux(15)
t = S.random_element()
widget = TableauWidget(t)
display(t)

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
from __future__ import print_function, absolute_import
from sage.combinat.tableau import *
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML
import traitlets

cell_layout = Layout(width='3em',height='2em', margin='0',padding='0')
css = HTML("<style>\n.blbutton { background-color: white; }\n.dwbutton {\n    border-collapse: collapse;\n    color: red;\n    border: 1px solid #666;\n}\n.left { border-right: 1px dotted #999; }\n.right { border-left: 1px dotted #999; }\n.bottom { border-top: 1px dotted #999; }\n.top { border-bottom: 1px dotted #999; }\n.green { background-color: lightgreen; }\n.blue { background-color: lightblue; }\n.pink { background-color: lightpink; }\n.yellow { background-color: lightyellow; }\n</style>")
try:
    display(css)
except:
    pass # We are not in a notebook


class TCell(Text):
    r"""Single cell for a Young Tableau."""

    def __init__(self, parent, coord, content):
        r"""
        Initializes a Tableau cell and compute its value.

        INPUT:

        - ``parent`` -- a TableauWidget
        - ``coord`` -- a tuple of coordinates (vertical, horizontal)
        - ``content`` -- an Integer value for the cell

        TESTS::

        sage: from sage_combinat_widgets.tableau_widget import TCell
        sage: c = TCell(None, (0,0), 5)
        sage: assert c.value == '5'
        """
        super(TCell, self).__init__(layout=cell_layout, continuous_update=False)
        self.parent = parent
        self.coord = coord
        self.content = content
        self.value = str(self.content)
        self.placeholder = str(content)

    @traitlets.observe('value')
    def update_cell(self, change):
        r"""
        TESTS::

        sage: from sage_combinat_widgets.tableau_widget import TCell
        sage: c = TCell(None, (0,0), 5)
        sage: from traitlets import Bunch
        sage: b = Bunch({'owner': c, 'new': u'10', 'old': u'5', 'name': 'value', 'type': 'change'})
        sage: assert b.new == '10'
        sage: c.update_cell(Bunch({'owner': c, 'new': u'10', 'old': u'5', 'name': 'value', 'type': 'change'}))
        sage: assert c.content == 10
        """
        if not change.new:
            return
        self.value = change.new
        self.content = int(self.value)


class TableauWidget(VBox):
    """Jupyter Widget for exploring a Young Tableau"""

    def __init__(self, tbl, display='en'):
        r"""
        TESTS::

            sage: from sage_combinat_widgets import TableauWidget
            sage: S = StandardTableaux(15)
            sage: t = S.random_element()
            sage: w = TableauWidget(t)
            sage: w.compute_status()
            sage: assert w.status == 'standard'
        """
        super(TableauWidget, self).__init__()
        self.tbl = tbl
        self.size = tbl.size()
        self.initial_lvalue = [[c for c in r] for r in self.tbl]
        self.label = Label("Tableau ready")
        self.cells = {}
        for r in self.tbl:
            for i in r:
                coord = (self.tbl.index(r), r.index(i))
                self.cells[coord] = TCell(self, coord, i)
                self.add_traits(**{'cell_%d_%d' % (coord) : traitlets.Unicode()})
                traitlets.link((self, 'cell_%d_%d' % (coord)), (self.cells[coord], 'value'))
        self.display_convention = display
        if self.display_convention == 'fr':
            rows = list(self.tbl)
            rows.reverse()
            self.children = [ self.label ] + [HBox(
                [self.cells[(self.tbl.index(r), r.index(i))] for i in r]
            ) for r in rows]
        else:
            self.children = [ self.label ] + [HBox(
                [self.cells[(self.tbl.index(r), r.index(i))] for i in r]
            ) for r in self.tbl]

    def validate(self, label='standard'):
        if label == 'semistandard':
            self.valid = self.tbl.is_semistandard()
        elif label == 'standard':
            self.valid = self.tbl.is_standard()
        else:
            self.valid = True

    def compute_status(self):
        if self.tbl.is_standard():
            self.status = 'standard'
        elif self.tbl.is_semistandard():
            self.status = 'semistandard'
        else:
            self.status = 'generic'

    def get_object(self):
        return self.tbl

    def set_object(self, tbl):
        self.tbl = tbl
        self.compute_status()

    @traitlets.observe(traitlets.All)
    def update_tableau(self, change):
        if not change.new or not change.name.startswith('cell_'):
            return
        assert(change.name.startswith('cell_') and '_' in change.name[5:])
        vpos = int(change.name.split('_')[1])
        hpos = int(change.name.split('_')[2])
        lvalue = [[c for c in r] for r in self.tbl]
        lvalue[vpos][hpos] = int(change.new)
        if lvalue == self.initial_lvalue:
            self.label.value = "Initial Tableau"
            return
        self.tbl = Tableau(lvalue)
        self.compute_status()
        self.label.value = self.status.capitalize()


class SemistandardTableauWidget(TableauWidget):
    """Jupyter Widget for exploring a Semistandard Tableau"""

    def __init__(self, tbl, display='en'):
        r"""
        TESTS::

        sage: from sage_combinat_widgets import *
        sage: S = SemistandardTableaux(15)
        sage: t = S.random_element()
        sage: widget = SemistandardTableauWidget(t)
        sage: assert widget.valid == True
        """
        super(SemistandardTableauWidget, self).__init__(tbl, display)
        self.validate('semistandard')


class StandardTableauWidget(TableauWidget):
    """Jupyter Widget for exploring a Standard Tableau"""

    def __init__(self, tbl, display='en'):
        r"""
        TESTS::

        sage: from sage_combinat_widgets import *
        sage: S = StandardTableaux(15)
        sage: t = S.random_element()
        sage: widget = StandardTableauWidget(t)
        sage: assert widget.valid == True
        sage: S = SemistandardTableaux(15)
        sage: t = S.random_element()
        sage: widget = StandardTableauWidget(t)
        sage: assert widget.valid == False
        """
        super(StandardTableauWidget, self).__init__(tbl, display)
        self.validate('standard')


class PartitionWidget(TableauWidget):
    """Jupyter Widget for exploring a Partition"""

    def __init__(self, partition):
        r"""

        TESTS::

        sage: from sage_combinat_widgets import *
        sage: from sage.combinat.partition import Partitions
        sage: p = Partitions(7)[5]
        sage: w = PartitionWidget(p)
        sage: assert w.valid == True
        """
        from sage.combinat.tableau import Tableau
        tbl = Tableau([[1]*partition[i] for i in range(len(partition))])
        super(PartitionWidget, self).__init__(tbl)
        self.validate('generic')

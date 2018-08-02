# -*- coding: utf-8 -*-
r"""
An editable Young Tableau for Sage Jupyter Notebook

EXAMPLES ::
    sage: from sage_combinat_widgets import TableauWidget
    sage: t = StandardTableaux(15).random_element()
    sage: widget = TableauWidget(t)

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
from __future__ import print_function, absolute_import
from sage.misc.bindable_class import BindableClass
from sage.combinat.tableau import *
from sage.all import SageObject
from ipywidgets import Layout, VBox, HBox, Text, Label, HTML
from .grid_widget import GridWidget
import traitlets

cell_layout = Layout(width='3em',height='2em', margin='0',padding='0')
css_lines = []
css_lines.append(".invisible {display: none; width: 0; height: 0;}")
css_lines.append(".visible {display: table}")
css_lines.append(".blbutton { background-color: white; }")
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

class TCell(Text):
    r"""Single cell for a Young Tableau."""

    def __init__(self, content, **kwargs):
        r"""
        Initializes a Tableau cell and compute its value.

        INPUT:

        - ``content`` -- an Integer value for the tableau cell

        TESTS::

            sage: from sage_combinat_widgets.tableau_widget import TCell
            sage: c = TCell(5)
            sage: assert c.value == '5'
        """
        super(TCell, self).__init__('', layout=cell_layout, continuous_update = False)
        self.content = content
        self.value = str(content)
        self.placeholder = str(content)

    @traitlets.observe('value')
    def update_cell(self, event):
        r"""
        TESTS::

        sage: from sage_combinat_widgets.tableau_widget import TCell
        sage: c = TCell(5)
        sage: from traitlets import Bunch
        sage: b = Bunch({'owner': c, 'new': u'10', 'old': u'5', 'name': 'value', 'type': 'change'})
        sage: assert b.new == '10'
        sage: c.update_cell(Bunch({'owner': c, 'new': u'10', 'old': u'5', 'name': 'value', 'type': 'change'}))
        sage: assert c.content == 10
        """
        if not event.new:
            return
        self.value = event.new
        self.content = int(self.value)

class TableauWidget(GridWidget):
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
        super(TableauWidget, self).__init__(tbl, TCell)
        self.size = tbl.size()
        self.initial_lvalue = [[c for c in r] for r in self.value]
        self.output = Label()
        self.output.add_class('invisible')
        self.display_convention = display
        if self.display_convention == 'fr':
            rows = list(self.value)
            rows.reverse()
            self.children = [ self.output ] + [HBox(
                [self.cells[(self.value.index(r), r.index(i))] for i in r]
            ) for r in rows]
        else:
            self.children = [ self.output ] + [HBox(
                [self.cells[(self.value.index(r), r.index(i))] for i in r]
            ) for r in self.value]

    def validate(self, label='standard'):
        if label == 'semistandard':
            self.valid = self.value.is_semistandard()
        elif label == 'standard':
            self.valid = self.value.is_standard()
        else:
            self.valid = True

    def compute_status(self):
        if self.value.is_standard():
            self.status = 'standard'
        elif self.value.is_semistandard():
            self.status = 'semistandard'
        else:
            self.status = 'generic'

    def get_object(self):
        return self.value

    def set_object(self, tbl):
        self.value = tbl
        self.compute_status()

    @traitlets.observe(traitlets.All)
    def update_tableau(self, event):
        if not event.new or not event.name.startswith('cell_'):
            return
        assert(event.name.startswith('cell_') and '_' in event.name[5:])
        vpos = int(event.name.split('_')[1])
        hpos = int(event.name.split('_')[2])
        lvalue = [[c for c in r] for r in self.value]
        lvalue[vpos][hpos] = int(event.new)
        if lvalue == self.initial_lvalue:
            self.output.value = "Initial Tableau"
            return
        self.value = Tableau(lvalue)
        self.compute_status()
        self.output.value = self.status.capitalize()
        if self.output.value:
            self.output.remove_class('invisible')
            self.output.add_class('visible')
        else:
            self.output.remove_class('visible')
            self.output.add_class('invisible')


class SemistandardTableauWidget(TableauWidget):
    """Jupyter Widget for exploring a Semistandard Tableau"""

    def __init__(self, tbl, display='en'):
        r"""
        TESTS::

        sage: from sage_combinat_widgets import SemistandardTableauWidget
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

        sage: from sage_combinat_widgets import StandardTableauWidget
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

        sage: from sage_combinat_widgets import PartitionWidget
        sage: from sage.combinat.partition import Partitions
        sage: p = Partitions(7)[5]
        sage: w = PartitionWidget(p)
        sage: assert w.valid == True
        """
        from sage.combinat.tableau import Tableau
        tbl = Tableau([[1]*partition[i] for i in range(len(partition))])
        super(PartitionWidget, self).__init__(tbl)
        self.validate('generic')

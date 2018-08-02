#!/usr/bin/env python
# coding: utf-8

from ipywidgets import ToggleButton, VBox, HBox, HTML, Layout
from .grid_widget import GridWidget
import contextlib
from traitlets import dlink, HasTraits, Bool, observe

css = HTML("<style>\n.blbutton { background-color: white; }\n.dwbutton {\n    border-collapse: collapse;\n    color: red;\n    border: 1px solid #666;\n}\n.left { border-right: 1px dotted #999; }\n.right { border-left: 1px dotted #999; }\n.bottom { border-top: 1px dotted #999; }\n.top { border-bottom: 1px dotted #999; }\n.green { background-color: lightgreen; }\n.blue { background-color: lightblue; }\n.pink { background-color: lightpink; }\n.yellow { background-color: lightyellow; }\n</style>")
try:
    display(css)
except:
    pass # We are not in a notebook


class ddlink(dlink):
    r"""Double directional link with logic = or/and/none.

    Double_source is a tuple of (source, target) tuples

    EXAMPLE::
        sage: from ipywidgets import ToggleButton
        sage: from sage_combinat_widgets.dominos import ddlink
        sage: b1 = ToggleButton(description = 'B1')
        sage: b2 = ToggleButton(description = 'B2')
        sage: b3 = ToggleButton(description = 'B3')
        sage: dl = ddlink(((b1, 'value'), (b2, 'value')), (b3, 'value'))
    """
    updating = False

    def __init__(self, double_source, target, logic=None, set_at_init=True):
        self.validate_tuple(target)
        self.logic = logic
        for source in double_source:
            self.validate_tuple(source)
        try:
            if set_at_init:
                if self.logic == 'and':
                    setattr(target[0], target[1],
                            getattr(double_source[0][0], double_source[0][1]) \
                            and getattr(double_source[1][0], double_source[1][1]))
                else:
                    setattr(target[0], target[1],
                            getattr(double_source[0][0], double_source[0][1]) \
                            or getattr(double_source[1][0], double_source[1][1]))
            else:
                pass
        finally:
            for source in double_source:
                source[0].observe(self._update, names=source[1])
                source[0].observe(self._update, names=source[1])
        self.target = target
        self.double_source = double_source
        self.intermediate_value = False # False / True / source.tooltip

    def validate_tuple(self, t):
        if not len(t) == 2:
            raise TypeError("Each linked traitlet must be specified as (HasTraits, 'trait_name'), not %r" % t)
        obj, trait_name = t
        if not isinstance(obj, HasTraits):
            raise TypeError("Each object must be HasTraits, not %r" % type(obj))
        if not trait_name in obj.traits():
            raise TypeError("%r has no trait %r" % (obj, trait_name))

    @contextlib.contextmanager
    def _busy_updating(self):
        self.updating = True
        try:
            yield
        finally:
            self.updating = False

    def _update(self, change):
        if self.updating:
            return
        with self._busy_updating():
            if self.logic == 'and':
                if self.intermediate_value == False: # aucun bouton pressé avant
                    self.intermediate_value = change.new
                elif self.intermediate_value == True: # 2 boutons pressés avant
                    setattr(self.target[0], self.target[1], change.new)
                    if change.new == False:
                        # prendre le tooltip de l'autre bouton
                        for s in self.double_source:
                            if s[0].tooltip != change.owner.tooltip:
                                self.intermediate_value = s[0].tooltip
                elif self.intermediate_value != change.owner.tooltip: # l'autre bouton a été pressé avant
                    setattr(self.target[0], self.target[1], change.new)
                    self.intermediate_value = change.new
            elif self.logic == 'or':
                if change.new == True:
                    setattr(self.target[0], self.target[1], True)
                    if self.intermediate_value == False:
                        self.intermediate_value = change.owner.tooltip
                    elif self.intermediate_value == True:
                        pass
                    elif self.intermediate_value != change.owner.tooltip:
                        self.intermediate_value = True
                else:
                    if self.intermediate_value != True:
                        setattr(self.target[0], self.target[1], False)
                    self.intermediate_value = False # FIXME

            else:
                setattr(self.target[0], self.target[1], change.new)

    def unlink(self):
        for source in self.double_source:
            source[0].unobserve(self._update, names=source[1])
        self.double_source, self.target = None, None


button_layout = Layout(width='5em',height='4em', margin='0')
blank_layout = Layout(width='5em',height='4em', margin='0', border='0')
grid_layout = Layout()
COLORS = ['green', 'blue', 'pink', 'yellow']
POSITIONS = ['left','right','top','bottom']

class BlankButton(ToggleButton):
    r"""A disabled button placeholder

    TESTS::
        sage: from sage_combinat_widgets.dominos import BlankButton
        sage: b = BlankButton()
    """

    def __init__(self):
        super(BlankButton, self).__init__(False, disabled=True)
        self.layout = blank_layout
        self.add_class('blbutton')

    def reset(self):
        pass

class DWButton(ToggleButton):
    r"""A button, part of a domino

    TESTS::
        sage: from sage_combinat_widgets.dominos import DWButton
        sage: b = DWButton('', placeholder='1,2')
        sage: assert b.coord == (1,2)
        sage: assert b.tooltip == '1,2'
    """
    def __init__(self, value, layout=None, placeholder=''): # parent, coord
        super(DWButton, self).__init__(False)
        self.layout = button_layout
        self.coord = tuple([int(i) for i in placeholder.split(',')]) # Is initialized within GridWidget.compute()
        self.tooltip = placeholder
        self.placeholder = None # We don't want a placeholder, just a tooltip
        self.add_class('dwbutton')
        self.link = None
        self.position = None

    def __str__(self):
        if self.position:
            return "%s (%s) %s" % (self.coord, self.position, str(self.value).upper())
        return "%s %s" % (self.coord, str(self.value).upper())

    def reset(self):
        """Reset button value"""
        self.value = False


class Domino (HasTraits):
    r"""Domino object, made with 2 (adjacent) DWButton widgets

    This object is not displayed in itself, but it has a trait

    TESTS::
        sage: from sage_combinat_widgets.dominos import DWButton, Domino
        sage: b1 = DWButton('', placeholder='1,2')
        sage: b2 = DWButton('', placeholder='1,3')
        sage: d = Domino(None, b1, b2)
        sage: assert d.first == b1
        sage: assert d.second == b2
        sage: assert d.direction == 'horizontal'
        sage: assert d.orientation == 1
        sage: assert d.first.position == 'left'
        sage: assert d.second.position == 'right'
        sage: assert d.cle == (1,2)
    """
    value = Bool()

    def __init__(self, parent, b1, b2):
        """A domino has a parent widget and is made of 2 buttons"""
        super(HasTraits, self).__init__()
        self.parent = parent
        self.cle = None
        self.first = b1
        self.second = b2
        self.buttons = (b1,b2)
        b1.link = dlink((b1, 'value'), (b2, 'value'))
        b2.link = dlink((b2, 'value'), (b1, 'value'))
        self.link = None
        self.direction = None
        self.orientation = None
        self.compute()

    def __str__(self):
        if self.value:
            return str(self.first) + ' -> ' + str(self.second) + " PRESSED"
        return str(self.first) + ' -> ' + str(self.second)

    @observe('value')
    def signale_clic(self, change):
        """Inform the parent widget"""
        if not change.new : # on ne s'intéresse qu'aux dominos enfoncés
            return
        self.parent.register(self, change)

    def compute(self):
        """Compute direction, orientation, color, buttons relative positions.
        Create double directional link from both buttons"""
        self.link = ddlink(((self.first, 'value'), (self.second, 'value')), (self, 'value'), logic='and', set_at_init=False) # Fresh ddlink
        if self.first.coord[0] == self.second.coord[0]: # same row
            self.direction = 'horizontal'
            if self.first.coord[1] + 1 == self.second.coord[1]:
                self.orientation = 1 #'left_to_right'
                self.first.position = 'left'
                self.second.position = 'right'
            elif self.first.coord[1] == self.second.coord[1] + 1:
                self.orientation = -1 #right_to_left
                self.first.position = 'right'
                self.second.position = 'left'
        elif self.first.coord[1] == self.second.coord[1]: # same column
            self.direction = "vertical"
            if self.first.coord[0] + 1 == self.second.coord[0]:
                self.orientation = 1 #top_to_bottom
                self.first.position = 'top'
                self.second.position = 'bottom'
            elif self.first.coord[0] == self.second.coord[0] + 1:
                self.orientation = -1 #bottom_to_top
                self.first.position = 'bottom'
                self.second.position = 'top'
        else: # not flippable
            return
        if self.orientation == 1:
            self.cle = self.first.coord
        else:
            self.cle = self.second.coord
        global COLORS, POSITIONS
        for cl in COLORS + POSITIONS:
            self.first.remove_class(cl)
            self.second.remove_class(cl)
        k = (self.cle[0] + self.cle[1]) % 2 # repérage pour la couleur
        if self.direction == 'horizontal':
            color = COLORS[k]
        else:
            color = COLORS[2+k]
        self.first.add_class(color)
        self.second.add_class(color)
        if self.first.position:
            self.first.add_class(self.first.position)
        if self.second.position:
            self.second.add_class(self.second.position)

    def is_pressed(self):
        """Is the domino pressed?"""
        return self.value

    def reset(self):
        """Full domino reset"""
        self.value = False
        self.link.unlink()
        self.first.reset()
        self.second.reset()

    def flip(self, other):
        """Flip self with some neighboring domino"""
        self.reset()
        other.reset()
        if self.orientation * other.orientation == 1: # Same orientation
            self.second, other.first = other.first, self.second
        else:
            self.second, other.second = other.second, self.second
        self.first.link.target = (self.second, 'value')
        self.second.link.target = (self.first, 'value')
        other.first.link.target = (other.second, 'value')
        other.second.link.target = (other.first, 'value')
        self.compute()
        other.compute()


class DominosWidget(GridWidget):
    r"""A widget for flipping dominos in a graph

    TESTS:
        sage: from sage_combinat_widgets import DominosWidget
        sage: from sage.all import graphs
        sage: g = graphs.GridGraph((5,7))
        sage: w = DominosWidget(g)

    """

    def __init__(self, g) :
        """
        Init a domino widget with shape g.
        Arguments = a graph g. (that will be the widget *value*)
        Could be a Grid2dGraph or AztecDiamondGraph

        EXAMPLE
        w = DominosWidget(graphs.GridGraph(5,7))
        """
        super(DominosWidget, self).__init__(g, DWButton, Bool)
        self.layout = grid_layout
        self.size = g.vertices()[-1]
        rows_idx = []
        rows = []
        row = []
        for v in self.value.vertices():
            if not v[0] in rows_idx:
                i = v[0]
                rows_idx.append(i)
                row = []
                rows.append(row)
                if v[1] != 0:
                    for k in range(v[1]):
                        row.append(BlankButton(self, (i,k)))
            j = v[1]
            row.append(DWButton(self, placeholder=str((i,j)[1:-1])))
        self.children = [HBox(r) for r in rows]
        self.dominos = None # clé = coord top-left du domino
        self.reset()

    def apparie(self, b1, b2):
        """Match buttons b1 and b2, that is: create a domino"""
        if b1 and b2:
            """Crée un domino, en laissant le domino tout calculer."""
            d = Domino(self, b1, b2)
            self.dominos[d.cle] = d
        else:
            print('This method requires 2 buttons!!', b1, b2)

    def reset(self):
        """Clear dominos and reset every button"""
        self.dominos = {}
        for hb in self.children:
            for dwb in hb.children:
                dwb.reset()

    def applique_couplage(self, couplage):
        """Apply a matching"""
        count = -1
        for (t1, t2) in couplage.items():
            self.apparie(self.children[t1[0]].children[t1[1]],
                         self.children[t2[0]].children[t2[1]])

    def flip(self, d1, d2):
        """d1 and d2 are dominos"""
        if d1 < d2:
            d2.flip(d1)
        else:
            d1.flip(d2)

    def find_possible_flips(self, cle):
        "Return list of neighbouring dominos, with same direction as self.dominos[cle]"
        possible_flips = []
        domino = self.dominos[cle]
        if domino.direction == 'horizontal':
            if cle[0] > 0:
                possible_flips.append((cle[0] - 1, cle[1]))
            if cle[0] < self.size[0]:
                possible_flips.append((cle[0] + 1, cle[1]))
        else:
            if cle[1] > 0:
                possible_flips.append((cle[0], cle[1] - 1))
            if cle[1] < self.size[1]:
                possible_flips.append((cle[0], cle[1] + 1))
        return possible_flips

    def register(self, domino, change):
        cle_domino = domino.cle
        if self.dominos.has_key(cle_domino):
            d1 = self.dominos[cle_domino]
            for cle_candidat in self.find_possible_flips(cle_domino):
                if self.dominos.has_key(cle_candidat) and self.dominos[cle_candidat].is_pressed():
                    d2 = self.dominos[cle_candidat]
                    self.flip(d1, d2)
                    self.dominos.pop(cle_domino)
                    self.dominos.pop(cle_candidat)
                    self.dominos[d1.cle] = d1
                    self.dominos[d2.cle] = d2
                    break # on ne flippe qu'une seule fois !

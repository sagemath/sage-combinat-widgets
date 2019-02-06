#!/usr/bin/env python
# coding: utf-8

from flipping_aztecdiamond import *
from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
from sage_combinat_widgets.grid_view_widget import GridViewWidget, ButtonCell, BlankButton
from ipywidgets import Layout, HTML
from traitlets import dlink, HasTraits, Bool, observe

smallblyt = Layout(width='12px',height='12px', margin='0', padding='0')
css = HTML("<style>.blankb {background-color: #fff}\n.gridbutton {border:1px solid #999 !important}\n.b1 {background-color: green}\n.b2 {background-color: blue}\n.b3 {background-color: red}\n.b4 {background-color: yellow}\n</style>")
try:
    display(css)
except:
    pass # We are not in a browser

COLORS = ['green', 'blue', 'pink', 'yellow']
POSITIONS = ['left','right','top','bottom']

class ddlink(dlink):
    """Double directional link with logic = or/and/none.
    Double_source is a tuple of (source, target) tuples
    Usage: b1 = Button(description = 'B1')
           b2 = Button(description = 'B2')
           b3 = Button(description = 'B3')
           dl = ddlink(((b1, 'value'), (b2, 'value')), (b3, 'value'))
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

    #@contextlib.contextmanager
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

#class OrderedDomino:
#    def __init__(self, first, second):
#        self.first = first
#        self.second = second
#        if first[0] == second[0]:
#            self.direction = 'horizontal'
#        else:
#            self.direction = 'vertical'
#    def parity(self, i):
#        return (self.first[0] % 2 + self.first[1] % 2 + i) % 2
#    def __repr__(self):
#        return "OrderedDomino from %s to %s" % (self.first, self.second)

class Domino(HasTraits):
    r"""Objet non représenté en lui-même, les 2
    boutons qu'il contient étant, eux, des widgets"""
    value = Bool()

    def __init__(self, parent, b1, b2):
        """A domino has a parent widget and is made of 2 buttons"""
        super(Domino, self).__init__()
        self.geometry = DominoGeometry(b1.position, b2.position)
        self.parent = parent
        self.key = None
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
        if not change.new : # consider only pressed dominos
            return
        self.parent.register(self, change)

    def compute(self):
        """Compute direction, orientation, color, buttons relative positions.
        Create double directional link from both buttons"""
        self.link = ddlink(((self.first, 'value'), (self.second, 'value')), (self, 'value'), logic='and', set_at_init=False) # Fresh ddlink
        if self.geometry.orientation == 1:
            self.key = self.first.position
        else:
            self.key = self.second.position
        #global COLORS, POSITIONS
        #for cl in COLORS + POSITIONS:
        #    self.first.remove_class(cl)
        #    self.second.remove_class(cl)
        #k = (self.key[0] + self.key[1]) % 2 # repérage pour la couleur
        #if self.direction == 'horizontal':
        #    color = COLORS[k]
        #else:
        #    color = COLORS[2+k]
        #self.first.add_class(color)
        #self.second.add_class(color)
        #if self.first.position:
        #    self.first.add_class(self.first.position)
        #if self.second.position:
        #    self.second.add_class(self.second.position)

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

def apply_matching(m, size, n):
    matching = {}
    shift_val = size - n
    def shift(t):
        return (t[0] + shift_val, t[1] + shift_val)
    for first, second in m:
        if first[0] < second[0] or first[1] < second[1]:
            d = OrderedDomino(shift(first), shift(second))
        else:
            d = OrderedDomino(shift(second), shift(first))
        matching[shift(first)] = d
        matching[shift(second)] = d
    return matching
def figure(size):
    g = AztecDiamondGraph(size)
    m = (((0,0),(0,1)), ((1,0), (1,1)))
    return g, m, apply_matching(m, size, 1)
def parity(pos):
    return (pos[0]%2 + pos[1]%2)%2
def similar_position(pos, ref):
    return ((pos[0]%2 + pos[1]%2)%2 == (ref[0]%2 + ref[1]%2)%2)

def make_cell_widget_class_index(matching, n):
    def cell_widget_class_index(pos):
        def calc_index_for_domino(d, n):
            if d.direction == 'horizontal':
                if not d.parity:
                    return 1
                else:
                    return 2
            else:
                if not d.parity:
                    return 3
                else:
                    return 4
        if pos in matching.keys():
            d = DominoGeometry(pos, matching[pos])
            return calc_index_for_domino(d, n)  
        return 0
    return cell_widget_class_index

class SmallButton(ButtonCell):
    def __init__(self, content, position, layout, **kws):
        super(SmallButton, self).__init__(content, position, layout, **kws)
        self.layout = smallblyt

class CSSButton(SmallButton):
    css_class = None
    def __init__(self, content, position, layout, **kws):
        super(CSSButton, self).__init__(content, position, layout, **kws)
        self.add_class(self.css_class)
def css_button(class_name):
    return type("{}Button" . format(class_name), (CSSButton,), {'css_class': class_name})

class SmallBlank(BlankButton):
    def __init__(self, layout, **kws):
        super(SmallBlank, self).__init__(**kws)
        self.layout = smallblyt

class DominosAdapter(GraphGridViewAdapter):
    def set_cell(self, obj, pos, val=True, dirty={}):
        r"""
        When we click on a graph cell,
        we prepare a possible flip
        or we try to complete the flip if it has been prepared previously
        """
        
class DominosWidget(GridViewWidget):
    """A widget with dominos"""

    def __init__(self, g):
        r"""
        Init a flipping dominos widget
        with flipping aztec diamond graph `g`
        """
        super(DominosWidget, self).__init__(g, adapter = GraphGridViewAdapter(),
                                            cell_widget_classes=[SmallButton, css_button('b1'), css_button('b2'), css_button('b3'), css_button('b4')],
                                            cell_widget_class_index=make_cell_widget_class_index(g.matching, g.order),
                                            blank_widget_class = SmallBlank)
        self.dominos = None # clé = coord top-left du domino
        self.reset()
        self.apply_matching(g.matching)

    def match(self, b1, b2):
        """Match buttons b1 and b2, that is: create a domino"""
        if b1 and b2:
            """Create a domino and let it do the work."""
            d = Domino(self, b1, b2)
            self.dominos[d.key] = d
        else:
            print('This method requires 2 buttons!!', b1, b2)

    def reset(self):
        """Clear dominos and reset every button"""
        self.dominos = {}
        #for hb in self.children:
        #    for dwb in hb.children:
        #        dwb.reset()

    def apply_matching(self, matching):
        """Apply a matching"""
        count = -1
        for (t1, t2) in matching.items():
            self.match(self.children[t1[0]].children[t1[1]],
                       self.children[t2[0]].children[t2[1]])

    def flip(self, d1, d2):
        """d1 and d2 are dominos"""
        if d1 < d2:
            d2.flip(d1)
        else:
            d1.flip(d2)

    def find_possible_flips(self, key): # FIXME mettre dans la classe métier
        "Return list of neighbouring dominos, with same direction as self.dominos[key]"
        d = self.dominos[key]
        pos1, pos2 = d.geometry.first, d.geometry.second
        if (pos1, pos2) in self.value.matching:
            m = (pos1, pos2)
        elif (pos2, pos1) in self.value.matching:
            m = (pos2, pos1)
        else:
            print("Strange!")
            return []
        possible_flips = []
        for n in d.geometry.neighbors():
            if n[0] in self.dominos:
                possible_flips.append((n[0]))
            elif n[1] in self.dominos:
                possible_flips.append((n[1]))
        for n in d.geometry.reverse().neighbors():
            if n[0] in self.dominos:
                possible_flips.append((n[0]))
            elif n[1] in self.dominos:
                possible_flips.append((n[1]))
        return possible_flips

    def register(self, domino, change):
        d_key = domino.key
        if self.dominos.has_key(d_key):
            d1 = self.dominos[d_key]
            for c_key in self.find_possible_flips(d_key): # candidate key
                if self.dominos.has_key(c_key) and self.dominos[c_key].is_pressed():
                    d2 = self.dominos[c_key]
                    self.flip(d1, d2)
                    self.dominos.pop(d_key)
                    self.dominos.pop(c_key)
                    self.dominos[d1.key] = d1
                    self.dominos[d2.key] = d2
                    break # only flip once!!


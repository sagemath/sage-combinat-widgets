#!/usr/bin/env python
# coding: utf-8

from .flipping_aztecdiamond import *
from sage_widget_adapters.graphs.graph_grid_view_adapter import GraphGridViewAdapter
from sage_combinat_widgets.grid_view_widget import GridViewWidget, ButtonCell, BlankButton, styled_button_cell
from ipywidgets import Layout
from traitlets import dlink, HasTraits, Bool, observe, All
from contextlib import contextmanager
from sage_combinat_widgets.grid_view_editor import extract_coordinates

smallblyt = Layout(width='12px',height='12px', margin='0', padding='0')


class FlippingDominosAdapter(GraphGridViewAdapter):

    remove_cell = None

    def set_cell(self, obj, pos, val, dirty={}):
        r"""
        When we click on a graph cell,
        we prepare a possible flip
        or we try to complete the flip if it has been prepared previously
        """
        # Find out the relevant matching for 'pos'
        d1 = obj.domino_for_position(pos)
        if dirty: # if i'm a neighbor, then flip and return a new obj ; else return an error
            # Consider the relevant matching(s)
            for p in dirty:
                if not dirty[p]: # check this position was pressed
                    continue
                d2 = obj.domino_for_position(p)
                if d2 == d1 or not d2 in d1.neighbors():
                    continue
                if d2 in d1.neighbors():
                    # Do the flip
                    obj.flip(d1, d2)
                    return obj
            return Exception("Please select a second domino!")
        else:
            return Exception("Please select a second domino!")


class mydlink(dlink):
    def _update(self, change):
        if self.updating:
            return
        if not self.target: # unlinked link
            return
        with self._busy_updating():
            setattr(self.target[0], self.target[1],
                    self._transform(change.new))


class Domino(object):
    r"""Objet non représenté en lui-même, les 2
    boutons qu'il contient étant, eux, des widgets"""

    def __init__(self, parent, b1, b2, link=True):
        """A domino has a parent widget and is made of 2 buttons"""
        b1.link = None
        b2.link = None
        b1.value = False
        b2.value = False
        super(Domino, self).__init__()
        self.value = False
        self.geometry = DominoGeometry(b1.position, b2.position)
        self.parent = parent
        self.key = None
        self.first = b1
        self.second = b2
        self.buttons = (b1,b2)
        self.direction = None
        self.orientation = None
        self.compute()
        if link:
            self.set_links()

    def __repr__(self):
        if self.value:
            return repr(self.first) + ' -> ' + repr(self.second) + " PRESSED"
        return repr(self.first) + ' -> ' + repr(self.second)

    def compute(self, css_classes=['b0', 'b1', 'b2', 'b3', 'b4']):
        """Compute buttons relative positions."""
        self.geometry.compute()
        if css_classes:
            for cl in css_classes:
                self.first.remove_class(cl)
                self.second.remove_class(cl)
            self.first.add_class(css_classes[self.geometry.index_for_display])
            self.second.add_class(css_classes[self.geometry.index_for_display])
        if self.geometry.orientation == 1:
            self.key = self.first.position
        else:
            self.key = self.second.position
        for cl in ['left','right','top','bottom']:
            self.first.remove_class(cl)
            self.second.remove_class(cl)
        if self.geometry.direction == 'horizontal':
            if self.geometry.orientation == 1:
                self.first.add_class('left')
                self.second.add_class('right')
            elif self.geometry.orientation == -1:
                self.first.add_class('right')
                self.second.add_class('left')
        elif self.geometry.direction == 'vertical':
            if self.geometry.orientation == 1:
                self.first.add_class('top')
                self.second.add_class('bottom')
            elif self.geometry.orientation == -1:
                self.first.add_class('bottom')
                self.second.add_class('top')

    def set_links(self):
        """Create double directional link from both buttons
        and for domino."""
        self.first.link = mydlink((self.first, 'value'), (self.second, 'value'))
        self.second.link = mydlink((self.second, 'value'), (self.first, 'value'))

    def is_pressed(self):
        """Is the domino pressed?"""
        return self.value

    def reset(self):
        """Full domino unlink"""
        self.first.link.unlink()
        self.first.link = None
        del self.first.link
        self.first.value = False
        self.second.link.unlink()
        self.second.link = None
        del self.second.link
        self.second.value = False

    def flip(self, other):
        """Flip self with some neighboring domino"""
        if other == self or other.geometry == self.geometry:
            return
        self.reset()
        other.reset()
        self.geometry.flip(other.geometry)
        self.compute()
        other.compute()


def make_cell_widget_class_index(g):
    def cell_widget_class_index(pos):
        d = g.domino_for_position(pos)
        if d:
            return d.calc_index_for_display()
        return 0
    return cell_widget_class_index


class FlippingDominosWidget(GridViewWidget):
    """A widget with dominos"""

    def __init__(self, g, css_classes=['b0', 'b1', 'b2', 'b3', 'b4']):
        r"""
        Init a flipping dominos widget
        with flipping aztec diamond graph `g`
        """
        self.css_classes = css_classes
        super(FlippingDominosWidget, self).__init__(g, adapter = FlippingDominosAdapter(),
                                            cell_layout = smallblyt,
                                            cell_widget_classes=[styled_button_cell(),
                                                                 styled_button_cell(style_name='b1'),
                                                                 styled_button_cell(style_name='b2'),
                                                                 styled_button_cell(style_name='b3'),
                                                                 styled_button_cell(style_name='b4'),
                                            ],
                                            cell_widget_class_index=make_cell_widget_class_index(g),
                                            blank_widget_class = BlankButton)

    def draw(self):
        self.dominos = {}
        super(FlippingDominosWidget, self).draw()
        self.apply_matching(self.value.matching)

    def match(self, b1, b2):
        """Match buttons b1 and b2, that is: create a domino"""
        try:
            assert issubclass(b1.__class__, ButtonCell) and issubclass(b2.__class__, ButtonCell)
        except:
            raise Exception('This method requires 2 buttons!! b1 = %s, b2 = %s' % (b1, b2) )
        """Create a domino and let it do the work. NB: the key should always be top-left."""
        d = Domino(self, b1, b2)
        self.dominos[d.key] = d

    def reset(self):
        """Clear dominos and reset every button"""
        self.dominos = {}

    def apply_matching(self, matching):
        """Apply a matching"""
        self.dominos = {}
        for d in matching:
            self.match(
                self.children[d.first[0]].children[d.first[1]],
                self.children[d.second[0]].children[d.second[1]]
            )

    def update(self):
        self.apply_matching(self.value.matching)
        for k,d in self.dominos.items():
            d.compute(self.css_classes)
            #d.set_value(False) # unpress buttons

    def domino_for_position(self, pos):
        geometry = self.value.domino_for_position(pos)
        for t in (geometry.first, geometry.second):
            if t in self.dominos:
                return self.dominos[t]

    @observe(All)
    def set_cell(self, change):
        if self.donottrack:
            return
        click_pos = extract_coordinates(change.name)
        domino = self.domino_for_position(click_pos)
        if not domino: # or domino.donottrack:
            return
        # The domino must be entirely pressed
        if not domino.first.value or not domino.second.value:
            #print("domino not pressed (", change.name, ")")
            #return # FIXME not clear what to do here
            pass
        else:
            #print("domino pressed (", change.name, ") ; dirty =", self.dirty)
            pass
        # The domino must have a pressed neighbor
        other = None
        if self.dirty:
            for pos in self.dirty:
                if other and other.geometry!=self.domino_for_position(pos).geometry:
                    raise Exception("on a un double dans les voisins pressés: %s et %s" % (
                        other.geometry, self.domino_for_position(pos).geometry))
                other = self.domino_for_position(pos)
                if other and not other.geometry in domino.geometry.neighbors():
                    other = None
                    continue # we don't have to reset everything, I guess(hope)
        if not other:
            # Feed the 'dirty' dict and return
            self.dirty[domino.geometry.first] = True
            self.dirty[domino.geometry.second] = True
            return
        # Do the flip
        super(FlippingDominosWidget, self).set_cell(change)
        # Unlink, reset values, delete dominos
        self.donottrack = True
        domino.reset()
        other.reset()
        del self.dominos[domino.key]
        del self.dominos[other.key]
        # Build our new dominos
        new_domino, new_other = None, None
        for g1 in self.value.matching:
            if g1.first == domino.geometry.first or g1.first == other.geometry.first:
                d1, d2 = domino.geometry, other.geometry
            if g1.first == domino.geometry.first:
                new_domino = Domino(
                    self,
                    self.children[g1.first[0]].children[g1.first[1]],
                    self.children[g1.second[0]].children[g1.second[1]],
                    link = False
                )
                self.dominos[new_domino.key] = new_domino
                for g2 in g1.neighbors():
                    if not g2 in self.value.matching:
                        continue
                    if (other.key in (g2.first, g2.second)) or \
                       (other.key == g1.second and domino.geometry.second in (g2.first, g2.second)):
                        new_other = Domino(
                            self,
                            self.children[g2.first[0]].children[g2.first[1]],
                            self.children[g2.second[0]].children[g2.second[1]],
                            link = False
                        )
                        self.dominos[new_other.key] = new_other
                        break
            elif g1.first == other.geometry.first:
                new_other = Domino(
                    self,
                    self.children[g1.first[0]].children[g1.first[1]],
                    self.children[g1.second[0]].children[g1.second[1]],
                    link = False
                )
                self.dominos[new_other.key] = new_other
                for g2 in g1.neighbors():
                    if not g2 in self.value.matching:
                        continue
                    if (domino.key in (g2.first, g2.second)) or \
                       (domino.key == g1.second and other.geometry.second in (g2.first, g2.second)):
                        new_domino = Domino(
                            self,
                            self.children[g2.first[0]].children[g2.first[1]],
                            self.children[g2.second[0]].children[g2.second[1]],
                            link = False
                        )
                        self.dominos[new_domino.key] = new_domino
                        break
            if new_domino and new_other:
                break
        # Check that new dominos are sound and the flip has actually been performed
        assert(new_domino is not None and new_other is not None)
        assert(new_domino.geometry != domino.geometry and new_other.geometry != other.geometry)
        # Compute the dominos
        new_domino.compute()
        new_other.compute()
        new_domino.set_links()
        new_other.set_links()
        # Reset
        self.reset_dirty()
        self.donottrack = False

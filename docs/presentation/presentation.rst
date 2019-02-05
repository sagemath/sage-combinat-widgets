Sage Combinat Widgets
=======================

A collection of **interactive widgets** for the *Jupyter* notebook

- graphically represent

- edit graphically and get the modified value

- can be used as building blocks in applications

- available for

  - (until now only grid-representable) combinatorial objects
  - (until now only grid-representable) graphs
  - matrices
  - write your own


Editing a Young Tableau
=========================

.. image:: images/scrn-tableau
    :scale: 50 %

`demo #1 <file:///home/odile/odk/sage/git/sage-combinat-widgets/docs/video/demo_youngtableau-short.ogv>`_


Using @interact
=================

.. image:: images/scrn-interact
    :scale: 50 %

`demo #2 <file:///home/odile/odk/sage/git/sage-combinat-widgets/docs/video/demo_interact.ogv>`_


Tossing Dominos
===============

*an implementation of*
`Pavages aleatoires par touillage <http://images.math.cnrs.fr/Pavages-aleatoires-par-touillage>`_

.. r2b_simplecolumns::
    :width: 0.95

    .. image:: images/TossingAlgorithm
        :scale: 30 %

    .. image:: images/TossedDiamond22
        :scale: 30 %
	   
`demo #3 <file:///home/odile/odk/sage/git/sage-combinat-widgets/docs/video/TossingDominos.ogv>`_


Your own widget: *Jeu de Taquin* example (1)
=============================================

*example based on*
`an experiment by Florent Hivert <https://github.com/hivert/SageWidgetExper>`_

.. image:: images/scrn-taquin
    :scale: 50 %

`demo #4 <file:///home/odile/odk/sage/git/sage-combinat-widgets/docs/video/demo_taquin.ogv>`_


Your own widget: *Jeu de Taquin* example (3)
==============================================

- Math code *(by F Hivert)*

.. code-block:: python

    def create_hole(self, corner):
	/.../
        inner_corners = self.inner_shape().corners()
        if tuple(corner) not in inner_corners:
            raise ValueError("corner must be an inner corner")
        self._hole = corner
        self._new_st = self.to_list()
        spotl, spotc = self._hole
        self._new_st[spotl][spotc] = True

    def slide(self):
        if self._hole is None:
            raise ValueError, "There is no hole"
        spotl, spotc = self._hole
        #Check to see if there is nothing to the right
        if spotc == len(self._new_st[spotl]) - 1:
            #Swap the hole with the cell below
            self._new_st[spotl][spotc] = self._new_st[spotl+1][spotc]
            self._new_st[spotl+1][spotc] = -1
            spotl += 1
        #Check to see if there is nothing below
        elif (spotl == len(self._new_st) - 1 or
              len(self._new_st[spotl+1]) <= spotc):
            #Swap the hole with the cell to the right
	    /.../

Your own widget: *Jeu de Taquin* example (3)
==============================================

- Adapter source code

.. code-block:: python
	
  # What happens when you click
  @classmethod
  def add_cell(cls, obj, pos, val, dirty={}):
      # Create a hole if there isn't
      if not obj.has_hole():
          obj.create_hole(pos)
      # Slide
      obj.slide()
      return obj

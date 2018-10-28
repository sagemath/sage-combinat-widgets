=====================
Sage Combinat Widgets
=====================

.. commented image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/sagemath/sage-combinat-widgets/master

Jupyter editable widgets for Sage Combinat:

- Standard/Semi-standard/Generic Tableau

  .. commented - Partition

Also : 

- Matrices
- Graphs

Installation
------------

Local install from source
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the source from the git repository::

    $ git clone https://github.com/sagemath/sage-combinat-widgets.git

Change to the root directory and run::

    $ sage -pip install --upgrade --no-index -v .

For convenience this package contains a [makefile](makefile) with this
and other often used commands. Should you wish too, you can use the
shorthand::

    $ make install

Usage
-----

Once the package is installed, you can use it in Sage Jupyter Notebook.

    from sage_combinat_widgets import GridViewWidget
    S = StandardTableaux(15).random_element()
    w = TableauWidget(t)
    w

See the `demo notebook <demo_GridViewWidget.ipynb>`_.

Tests
-----

Once the package is installed, one can use the SageMath test system
configured in ``setup.py`` to run the tests::

    $ sage setup.py test

This is just calling ``sage -t`` with appropriate flags.

Shorthand::

    $ make test

Documentation
-------------

The documentation of the package can be generated using Sage's
``Sphinx`` installation::

    $ cd docs
    $ sage -sh -c "make html"

Shorthand::

    $ make doc

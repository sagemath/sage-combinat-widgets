=====================
Sage Combinat Widgets
=====================

A few widgets for Sage Combinat:
- Standard/Semi-standard/Generic Tableau
- Partition

Installation
------------

Local install from source
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the source from the git repository::

    $ git clone https://github.com/nthiery/odile/sage_combinat_widgets.git

Change to the root directory and run::

    $ sage -pip install --upgrade --no-index -v .

For convenience this package contains a [makefile](makefile) with this
and other often used commands. Should you wish too, you can use the
shorthand::

    $ make install

Usage
-----

Once the package is installed, you can use it in Sage Jupyter Notebook.

    from sage_combinat_widgets import TableauWidget
    S = StandardTableaux(15)
    t = S.random_element()
    w = TableauWidget(t)
    display(w)

See the `demo notebook <demo_tableau_widget.ipynb>`_.


Source code
-----------

All source code is stored in the folder ``sage_combinat_widget`` using the same name as the
package. This is not mandatory but highly recommended for clarity. All source folder
must contain a ``__init__.py`` file with needed includes.

Tests
-----

Once the package is installed, one can use the SageMath test system
configured in ``setup.py`` to run the tests::

    $ sage setup.py test

This is just calling ``sage -t`` with appropriate flags.

Shorthand::

    $ make test

=====================
Sage Combinat Widgets
=====================

.. image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/sagemath/sage-combinat-widgets/master

Jupyter editable widgets for Sagemath combinatorial objects:

- Partition & Skew Partition
- Standard/Semi-standard/Generic Tableau & Skew Tableau
- Parallelogram Polyomino

Also : 

- Matrices
- grid-representable Graphs

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

Acknowledgments
---------------

.. |EULogo| image:: http://opendreamkit.org/public/logos/Flag_of_Europe.svg
    :width: 25
    :alt: EU logo

* |EULogo| This package was created under funding of the Horizon 2020 European Research Infrastructure project
  `OpenDreamKit <https://opendreamkit.org/>`_ (grant agreement `#676541 <https://opendreamkit.org>`_).

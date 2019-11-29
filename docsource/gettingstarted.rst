********************************************************************************
Getting Started
********************************************************************************

.. note::

    If you intend to install ``compas_assembly`` in a virtual environment,
    which you should, make sure to activate the environment first.


Install dependencies
====================

.. code-block:: bash

    conda install -c conda-forge COMPAS
    conda install -c conda-forge shapely
    conda install -c conda-forge PySide2
    conda install -c conda-forge PyOpenGL

.. code-block:: bash

    pip install git+https://github.com/compas-dev/compas_viewers.git#egg=compas_viewers


Install the package
===================

.. code-block:: bash

    pip install git+https://github.com/BlockResearchGroup/compas_assembly.git#egg=compas_assembly


Check installation
==================

Start an interactive Python interpreter on the commad line and import the packages.

.. code-block:: python

    >>> import compas
    >>> import shapely
    >>> import PySide2
    >>> import PyOpenGL
    >>> import compas_viewers
    >>> import compas_assembly


Install package for Rhino
=========================

.. code-block:: python

    python -m compas_rhino.install -p compas compas_rhino compas_assembly

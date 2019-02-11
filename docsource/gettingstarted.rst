********************************************************************************
Getting Started
********************************************************************************

.. highlight:: bash


Requirements
============

* `Anaconda <https://www.anaconda.com/download>`_
* `Git <https://git-scm.com/downloads>`_


Installation
============

.. note::

    If you intend to install ``compas_assembly`` in a virtual environment,
    make sure to activate the environment first.


1. Install dependencies
-----------------------

**On Mac**

::

    $ pip install shapely


**On Windows**

::

    $ conda install -c conda-forge shapely


2. Install the package
----------------------

.. note::

    This will also install COMPAS and its dependencies, if necessary.

::

    $ pip install git+https://github.com/BlockResearchGroup/compas_assembly.git


3. Check installation
---------------------

Start an interactive Python session in the Terminal.

::

    >>> import compas
    >>> import compas_assembly


4. Install package for Rhino
----------------------------

::

    $ python -m compas_rhino.install -p compas_assembly


5. Install solvers
------------------

To evaluate the stability of an assembly or to compute the contact forces at the
interfaces between the blocks required for static equilibrium, you will need to
install an equilibrium solver.

* https://github.com/BlockResearchGroup/compas_rbe


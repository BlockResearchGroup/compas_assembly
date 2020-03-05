********************************************************************************
Getting Started
********************************************************************************

Create an environment
=====================

.. raw:: html

    <div class="card">
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#replace_python_windows">Windows</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#replace_python_osx">OSX</a>
                </li>
            </ul>
        </div>
        <div class="card-body">
            <div class="tab-content">

.. raw:: html

    <div class="tab-pane active" id="replace_python_windows">

.. code-block:: bash

    conda create -n dem python=3.7

.. raw:: html

    </div>
    <div class="tab-pane" id="replace_python_osx">

.. code-block:: bash

    conda create -n dem python=3.7 python.app

.. raw:: html

    </div>
    </div>
    </div>
    </div>

.. note::

    You can use any name you like for the environment, except ``base``,
    which is the name of the root environment of your conda installation.
    In the instructions here, i have used the name "dem" of "Discrete Element Modeling".


Activate the environment
========================

.. code-block:: bash

    conda activate dem


In all the next steps, it is assumed that this environment is active.


Install dependencies
====================

.. code-block:: bash

    conda install -c conda-forge COMPAS
    conda install -c conda-forge shapely


Install the package
===================

To install directly from GitHub, do

.. code-block:: bash

    pip install git+https://github.com/BlockResearchGroup/compas_assembly.git#egg=compas_assembly


To install from a local source repo, navigate to the root of the repo, and do

.. code-block:: bash

    pip install -e .


Check installation
==================

Start an interactive Python interpreter on the commad line
and import the packages to check if the installation procedure was successful.

.. code-block:: python

    >>> import compas
    >>> import compas_assembly


Install package for Rhino
=========================

.. code-block:: bash

    python -m compas_rhino.install -p compas compas_rhino compas_assembly


Install equilibrium solvers
===========================

To compute the equilibrium of an assembly you will need a solver.
``compas_assembly`` is compatible with multiple solver packages:

* ``compas_rbe``
* ``compas_3dec``
* ``compas_prd``

Currently, only ``compas_rbe`` is publically available.
Please follow the installation instructions in the ``compas_rbe`` docs:
https://blockresearchgroup.github.io/compas_rbe/

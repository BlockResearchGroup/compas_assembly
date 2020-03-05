********************************************************************************
Getting Started
********************************************************************************

Create an environment
=====================

We highly recommend to install ``compas_assembly`` and related packages in a
separate conda environment. In this guide, we will create and use an
environmenment based on Python 3.7 with the name "dem", referring to
"Discrete Element Modelling", but you can use any other name you like
(except for "base", which is the name of the root environment of your conda
installation).

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

    conda create -n dem -c conda-forge python=3.7 COMPAS shapely

.. raw:: html

    </div>
    <div class="tab-pane" id="replace_python_osx">

.. code-block:: bash

    conda create -n dem -c conda-forge python=3.7 python.app COMPAS shapely

.. raw:: html

    </div>
    </div>
    </div>
    </div>


Activate the environment
========================

The root environment is active by default.
Therefore, you should not forget to activate the "dem" environment whenever
you want to work with ``compas_assembly`` and its related packages.

.. code-block:: bash

    conda activate dem


Install compas_assembly
=======================

There are no released versions of ``compas_assembly`` yet.
To install ``compas_assembly`` directly from GitHub, do

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


Also check the version of COMPAS

.. code-block:: python

    >>> compas.__version__
    '0.15.4'


Install compas_assembly for Rhino
=================================

.. code-block:: bash

    python -m compas_rhino.install -p compas compas_rhino compas_assembly


Install compas_rbe
==================

``compas_rbe`` is an equilibrium solver for ``compas_assembly``.
To install ``compas_rbe`` directly from GitHub, do

.. code-block:: bash

    pip install git+https://github.com/BlockResearchGroup/compas_rbe.git#egg=compas_rbe


To install ``compas_rbe`` from a local source repo,
navigate to the root of the repo and do

.. code-block:: bash

    pip install -e .


Finally, ``compas_rbe`` supports multiple backends for solving the quadratic
optimisation problem formulated in the Rigid Block Equilibrium problem.

.. code-block:: bash

    conda install -c conda-forge cvxpy cvxopt
    conda install -c ibmdecisionoptimization cplex


Note that the CPLEX installed via conda-forge is the Community Edition,
which means it is limited to 1000 variables and constraints.
Although this sounds like a lot, with ``compas_rbe`` you will hit these limits
quite quickly. Since the CPLEX backend is by far the fastest and most robust
option for ``compas_rbe``, we recommend installing the Academic Edition
if you are affiliated to an academic institution.

Instructions for installing CPLEX and it's Python API can be found here:

https://www.ibm.com/support/knowledgecenter/SSSA5P_12.8.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/setup_overview.html

If you have problems with the installation of the Academic Edition,
some solutions can be found here:

https://github.com/compas-Workshops/WS_Taubman/issues/1

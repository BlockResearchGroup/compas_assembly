********************************************************************************
Installation
********************************************************************************

Basic Installation
==================

We highly recommend to install :mod:`compas_assembly` in a
separate ``conda`` environment. In this guide, we will create and use an
environmenment based on Python 3.7 with the name "dem", referring to
"Discrete Element Modelling", but you can use any other name you like
(except for "base", which is the name of the root environment of your conda
installation).

.. code-block:: bash

    conda create -n dem -c conda-forge python=3.7 COMPAS shapely
    conda activate dem
    pip install compas_assembly

To verify that the procedure was successful, import the installed package.
That's it! If no errors appear, you are ready to start working.

.. code-block:: python

    python -c "import compas_assembly"

Alternatives
------------

If you prefer installing ``compas_assembly`` directly from GitHub, replace ``pip install compas_assembly`` with

.. code-block:: bash

    pip install git+https://github.com/BlockResearchGroup/compas_assembly.git#egg=compas_assembly

Or, to install from a local source repo, navigate to the root of the repo, and do

.. code-block:: bash

    pip install -e .


Install the viewer
==================

If you don't need the functionality of CAD software,
but simply want to be able to visualize assemblies and various aspects related to their stability and collapse behaviour,
you can use the COMPAS viewer instead.

.. code-block:: bash

    conda install -n dem compas_view2

For more information about the viewer, `check out the docs <https://compas.dev/compas_view2/latest/index.html>`_.


Install :mod:`compas_assembly` for Rhino
==========================================

:mod:`compas_assembly` can be installed in Rhino like any other COMPAS package.
See the `Getting Started instructions for Rhino <https://compas.dev/compas/latest/gettingstarted/rhino.html>`_ in the main COMPAS docs for more information.

.. code-block:: bash

    python -m compas_rhino.install -p compas compas_rhino compas_assembly

Note that, if Rhino was running while the above command was executed, you have to restart Rhino before the changes have an effect.


Install :mod:`compas_assembly` for Blender
==========================================

To use :mod:`compas_assembly` in Blender, you have to install it in your COMPAS Blender environment,
`as described here <https://compas.dev/compas/latest/gettingstarted/blender.html>`_.


Install equilibrium solvers
===========================

:mod:`compas_assembly` provides data structures and algorithms for managing the relationships between the individual elements of an assembly.
However, it doesn't provide any solvers for assessing the stability of assemblies or, for example, for assessing the impact on stability of the application
of external loads or differential settlements at the support.
To enable this kind of functionality, you have to install additional packages.
Currently, the following equilibrium solvers are compatible with :mod:`compas_assembly`.

* :mod:`compas_rbe`
* :mod:`compas_cra`
* :mod:`compas_prd`
* :mod:`compas_3dec`

Installation instructions are available on the respective project pages.

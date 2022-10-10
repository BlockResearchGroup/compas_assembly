********************************************************************************
Installation
********************************************************************************

Installation with conda
=======================

.. code-block:: bash

    conda create -n dem -c conda-forge python=3.9 compas compas_occ compas_view2 shapely --yes
    conda activate dem
    pip install compas_assembly


Install :mod:`compas_assembly` for Rhino
==========================================

:mod:`compas_assembly` can be installed in Rhino like any other COMPAS package.
See the `Getting Started instructions for Rhino <https://compas.dev/compas/latest/gettingstarted/rhino.html>`_ in the main COMPAS docs for more information.

.. code-block:: bash

    python -m compas_rhino.install

Note that, if Rhino was running while the above command was executed, you have to restart Rhino before the changes have an effect.


Install :mod:`compas_assembly` for Blender
==========================================

Instructions coming soon...


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

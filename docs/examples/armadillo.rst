***************
Armadillo Vault
***************

.. figure:: /_images/armadillo_02_interfaces.png
    :figclass: figure
    :class: figure-img img-fluid

Construct an assembly data structure for the Armadillo Vault that can be used for equilibrium calculations, generation of fabrication data, or assembly simulationos.
the procedure consists of two steps

1. Create an empty assembly and add block meshes.
2. Identify the interfaces between the blocks.

The required input for step 1 can be downloaded here:
:download:`armadillo_meshes.json <armadillo/armadillo_meshes.json>`.
If you place this file in the same folder as the script, the code will work as-is...


Create Assembly and Add Blocks
==============================

.. figure:: /_images/armadillo_01_assembly.png
    :figclass: figure
    :class: figure-img img-fluid

.. literalinclude:: armadillo/01_armadillo_assembly.py
    :language: python


Identify Interfaces
===================

.. figure:: /_images/armadillo_02_interfaces.png
    :figclass: figure
    :class: figure-img img-fluid

.. literalinclude:: armadillo/02_armadillo_interfaces.py
    :language: python


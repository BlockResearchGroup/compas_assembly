*****************
Crossvault
*****************

.. figure:: /_images/crossvault_02_interfaces.png
    :figclass: figure
    :class: figure-img img-fluid

Construct an assembly data structure of a cross-vault that can be used for equilibrium calculations, generation of fabrication data, or assembly simulationos.
The procedure consists of two steps

1. Create an empty assembly and add block meshes.
2. Identify the interfaces between the blocks.

The required input for step 1 can be downloaded here:
:download:`crossvault_meshes.json <crossvault/crossvault_meshes.json>`.
If you place this file in the same folder as the script, the code will work as-is...


Create Assembly and Add Blocks
==============================

.. figure:: /_images/crossvault_01_assembly.png
    :figclass: figure
    :class: figure-img img-fluid

.. literalinclude:: crossvault/01_crossvault_assembly.py
    :language: python


Identify Interfaces
===================

.. figure:: /_images/crossvault_02_interfaces.png
    :figclass: figure
    :class: figure-img img-fluid

.. literalinclude:: crossvault/02_crossvault_interfaces.py
    :language: python

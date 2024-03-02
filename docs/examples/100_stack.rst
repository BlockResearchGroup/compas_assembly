********************************************************************************
Leaning Stack of Blocks
********************************************************************************

.. figure:: /_images/100_stack.png

Summary
=======

First, we construct an assembly from a stack of blocks.
Each block is slightly shifted with respect to the previous one, to creating a leaning tower.
Then, we identify the interfaces of the assembly,
and compute the contact forces between the blocks that result in static equilibrium with gravitational loads.
Finally, we export the assembly to a JSON file and visualize the result with the DEM Viewer.


Equilibrium
===========

Note that the contact forces (in blue) increase towards the bottom of the stack,
due to the increasing weight.

The result forces (in green) between block 0 and 1, between 1 and 2, and between 2 and 3
are not contained in the interfaces between those blocks.
As a result, the stack can only be stable by introducing equilibriating "glue" forces (in red)
at those interfaces.


Code
====

.. note::

    This example uses ``compas_cra`` for the equilibrium calculations.
    If you don't have ``compas_cra`` installed,
    or simply don't want to compute the contact forces,
    just comment out lines 3 and 50.


.. literalinclude:: 100_stack.py
    :language: python

********************************************************************************
Two Blocks
********************************************************************************

.. figure:: /_images/000_two-blocks.png

Summary
=======

First, we construct an assembly from two simple blocks, one on top of the other.
Then, we identify the interfaces of the assembly,
and compute the contact forces between the blocks that result in static equilibrium with gravitational loads.
Finally, we export the assembly to a JSON file and visualize the result with the DEM Viewer.


Equilibrium
===========

The equilibrium is simple.
The forces are equally distributed over the four corners of the interface,
and the resultant is throught center.
There is no friction.

.. note::

    Note that this example uses ``compas_cra`` for the equilibrium calculations.
    If you don't have ``compas_cra`` installed,
    or simply don't want to compute the contact forces,
    just comment out lines 3 and 48.


Code
====

.. literalinclude:: 000_two-blocks.py
    :language: python

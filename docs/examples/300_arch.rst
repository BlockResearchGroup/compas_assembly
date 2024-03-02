********************************************************************************
A Semicircular Arch
********************************************************************************

.. figure:: /_images/300_arch.png

Summary
=======

First, we construct an assembly from a template for semicircular arches.
Then, we identify the interfaces of the assembly,
and compute the contact forces between the blocks that result in static equilibrium of the assembly
with gravitational loads.
Finally, we export the assembly to a JSON file and visualize the result with the DEM Viewer.


Equilibrium
===========

Coming...


Code
====

.. note::

    Note that this example uses ``compas_cra`` for the equilibrium calculations.
    If you don't have ``compas_cra`` installed,
    or simply don't want to compute the contact forces,
    just comment out lines 3 and 41.


.. literalinclude:: 300_arch.py
    :language: python

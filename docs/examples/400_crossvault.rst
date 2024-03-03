********************************************************************************
Crossvault
********************************************************************************

.. figure:: /_images/400_crossvault.png

Summary
=======

First, we construct the assembly from a list of meshes representing the blocks.
The JSON file containing the meshes is available here: :download:`crossvault.json <crossvault.json>`.
Then, we detect the interfaces between the blocks, and compute an approximate equilibrium solution.
Finally, we export the assembly and visualize the result.


Equilibrium
===========

Coming...


.. note::

    Note that this example uses ``compas_cra`` for the equilibrium calculations.
    If you don't have ``compas_cra`` installed,
    or simply don't want to compute the contact forces,
    just comment out lines 3, 4 and 58.


Code
====

.. literalinclude:: 400_crossvault.py
    :language: python

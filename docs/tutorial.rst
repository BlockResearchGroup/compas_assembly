********************************************************************************
Tutorial
********************************************************************************

.. rst-class:: lead

:mod:`compas_assembly` contains data structures and algorithms for modelling the individual
elements of Discrete Element Assemblies or Models, and the interactions and relationships between them.
The package itself **DOES NOT** provide tools or solvers for computing contact forces between the element
or for analysing the stability of entire assemblies.
To enable such calculations, you have to install additional solver packages such as :mod:`compas_rbe`.

Construct an Assembly
=====================

The most basic usage of :mod:`compas_assembly` is to create an empty assembly and add blocks.
For example, here we create an assembly of two blocks stacked on top of each other.

.. code-block:: python

    from math import radians
    from compas.geometry import Box, Translation, Rotation
    from compas_assembly.datastructures import Block
    from compas_assembly.datastructures import Assembly

    b1 = Block.from_shape(Box.from_width_height_depth(1, 1, 1))

    T = Translation.from_vector([0, 0, 1])
    R = Rotation.from_axis_and_angle([0, 0, 1], radians(45))

    b2 = b1.transformed(T * R)

    assembly = Assembly()

    assembly.add_block(b1)
    assembly.add_block(b2)

    assembly.to_json('assembly.json')


Visualization
=============

The assembly from the code above can be visualized in Rhino/GH or Blender using artists.
At this point, the assembly contains the added blocks, but no information is available about the interfaces.
There for the network (graph) representing the assembly has nodes (one per block),
but no edges, because the relationship between the blocks is not yet known.

Rhino
-----

.. code-block:: python

    from compas_assembly.rhino import AssemblyArtist

    artist = AssemblyArtist(assembly, layer='Assembly')
    artist.clear_layer()

    artist.draw_nodes()
    artist.draw_blocks()

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


Blender
-------

.. code-block:: python

    import compas_blender
    from compas_assembly.blender import AssemblyArtist

    compas_blender.clear()

    artist = AssemblyArtist(assembly)

    artist.draw_nodes()
    artist.draw_blocks()

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


COMPAS Viewer
-------------

The COMPAS viewer doesn't provide direct support for assemblies yet,
but they can be visualized using a combination of a NetworkObject and multiple MeshObjects.

.. code-block:: python

    from compas_view2.objects import Object, NetworkObject, MeshObject
    from compas_view2.app import App

    Object.register(Block, MeshObject)
    Object.register(Assembly, NetworkObject)

    viewer = App()
    viewer.add(assembly)
    for node in assembly.nodes():
        block = assembly.node_attributes(node, 'block')
        viewer.add(block)
    viewer.show()

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


Interfaces
==========

The 2-block assembly above is simply a collection of blocks.
Relationships between the blocks have not been established, yet.
This can be done manually, if the relationships are know,
or using interface detection with :func:`assembly_identify_interfaces_numpy`.
Note that only face-face interfaces are supported.

The interface identification algorithm uses ``numpy`` in the background (hence the suffix ``_numpy``).
In CPython environments the function can be used directly.
For example, in Blender or in combination with View2.

.. code-block:: python

    from compas_assembly.datastructures import assembly_identify_interfaces_numpy

    assembly_identify_interfaces_numpy(assembly)

In Rhino, ``numpy`` based algorithms have to be used through a RPC proxy of :mod:`compas.rpc`.
For more information, see `the main COMPAS docs <https://compas.dev/compas/latest/tutorial/rpc.html>`_.

.. code-block:: python

    from compas.rpc import Proxy

    proxy = Proxy('compas_assembly.datastructures')

    # proxy objects can't (yet) update objects in place
    # it always returns the result
    assembly = proxy.assembly_identify_interfaces(assembly)

In both cases, the relationships between the blocks are now encoded on the edges of the
assembly network, and the block connectivity and interface geometry can be visualised.

.. code-block:: python

    artist = AssemblyArtist(assembly)

    artist.draw_nodes()
    artist.draw_blocks(show_faces=False)
    artist.draw_edges()
    artist.draw_interfaces()

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


Data and Serialization
======================

Both the assembly and the individual blocks implement the COMPAS data framework.
This means that entire assemblies can be saved to or loaded from a JSON file,
and used in combination with Remote Procedure Calls from :mod:`compas.rpc` as we have seen earlier.

.. code-block:: python

    # script A

    assembly.to_json('assembly.json')

.. code-block:: python

    # script B

    assembly = Assembly.from_json('assembly.json')


Assembly Templates
==================

In a research context, it is often useful to be able to generate variations of assemblies of well-known
structural typpologies, for example to generate sample data during the development of a new algorithm.
For this, :mod:`compas_assembly` includes a growing library of templates.

.. code-block:: python

    rise = 5
    span = 10
    thickness = 0.7
    depth = 0.5
    n = 40

    arch = Arch(rise, span, thickness, depth, n)
    assembly = Assembly.from_template(arch)

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


Next Steps
==========

Check out the `Examples <https://blockresearchgroup.github.io/compas_assembly/latest/examples>`_ section of the docs
for examples of more elaborate assemblies.

Or have a look at the openMasonry project and some of the equilibrium solvers compatible with :mod:`compas_assembly`.

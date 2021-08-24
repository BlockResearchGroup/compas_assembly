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


Visualization
=============

To visualize an assembly in Rhino or Blender, you can use the corresponding artists.
For visualization outside of a CAD environment, you can use the COMPAS viewer.

Rhino
-----

.. code-block:: python

    import compas_rhino
    from compas_assembly.rhino import AssemblyArtist

    compas_rhino.clear()

    artist = AssemblyArtist(assembly)

    artist.draw_nodes()
    artist.draw_blocks()
    artist.draw_edges()
    artist.draw_interfaces()

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
    artist.draw_edges()
    artist.draw_interfaces()

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


Viewer
------

The assembly viewer is a work in progress and adds a thin layer around the standard COMPAS viewer.
With the standard viewer, you can visualize an assembly as follows.

.. code-block:: python

    from compas_assembly.datastructures import Block
    from compas_assembly.datastructures import Assembly

    from compas_view2.objects import Object
    from compas_view2.objects import NetworkObject
    from compas_view2.objects import MeshObject
    from compas_view2.objects import Collection
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

The assembly viewer provides a more user-friendly experience.
However, the viewer is still in early stages of developmenbt and therefore the API and usage patterns are subject to frequent change...

.. code-block:: python

    from compas_assembly.viewer import Viewer

    viewer = Viewer()
    viewer.add(assembly)
    viewer.show()


Interfaces
==========

The 2-block assembly above is simply a collection of blocks.
Relationships between the blocks have not been established yet.
This is done using interface detection.
Note that currently only face-face interfaces are supported.

.. code-block:: python

    from compas_assembly.datastructures import assembly_identify_interfaces_numpy

    assembly_identify_interfaces_numpy(assembly)

Note that the interface identification algorithm uses Numpy in the background (hence the suffix ``_numpy``).
In CPython environments this is not a problem and the function can be used directly.
For example, in Blender.

.. code-block:: python

    assembly_identify_interfaces_numpy(assembly)

In Rhino, Numpy based algorithms have to be used through the Remote Procedure Calls of :mod:`compas.rpc`.
For more information, see `the main COMPAS docs <https://compas.dev/compas/latest/tutorial/rpc.html>`_.

.. code-block:: python

    from compas.rpc import Proxy

    proxy = Proxy('compas_assembly.datastructures')
    assembly_identify_interfaces = proxy.assembly_identify_interfaces_numpy

    assembly = assembly_identify_interfaces(assembly)

In both cases, the relationships between the blocks are now encoded on the edges of the
assembly network or graph, and the interface geometry can be visualised.

.. code-block:: python

    artist = AssemblyArtist(assembly)

    artist.draw_nodes()
    artist.draw_blocks(show_faces=False)
    artist.draw_edges()
    artist.draw_interfaces()

.. figure:: /_images/
    :figclass: figure
    :class: figure-img img-fluid


Equilibrium Calculations
========================

With the interfaces identified, only the support conditions still need to be defined before the equilibrium
of an assembly can be computed using one of the available solvers.
In our example we select the bottom block.

.. code-block:: python

    assembly.node_attribute(0, 'is_support', True)


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

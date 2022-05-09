from compas.geometry import Point, Line
from compas.datastructures import Mesh

from compas_assembly.datastructures import Block
from compas_assembly.datastructures import Assembly
from compas_assembly.algorithms import assembly_interfaces_numpy
from compas_assembly.geometry import Arch

from compas_view2.app import App
from compas_view2.objects import Object
from compas_view2.objects import MeshObject

# construct an arch assembly

num_blocks = 40
arch = Arch(rise=5, span=10, thickness=0.7, depth=0.5, n=num_blocks)
assembly = Assembly.from_geometry(arch)

# define the boundary conditions

assembly.graph.node_attribute(0, 'is_support', True)
assembly.graph.node_attribute(num_blocks-1, 'is_support', True)

# identify the interfaces

assembly_interfaces_numpy(assembly)

# ==============================================================================
# Visualisation
# ==============================================================================

Object.register(Block, MeshObject)

viewer = App()

for node in assembly.graph.nodes():
    point = assembly.node_point(node)
    block = assembly.node_block(node)

    viewer.add(point, size=10, color=(0, 0, 0))

    viewer.add(block,
               show_faces=assembly.graph.node_attribute(node, 'is_support'),
               show_edges=True,
               facecolor=(1.0, 0, 0))

for edge in assembly.edges():
    line = Line(*assembly.edge_coordinates(edge))
    interface = assembly.edge_interface(edge)

    viewer.add(line, linewidth=3, color=(0, 0.7, 0))

    viewer.add(Mesh.from_polygons([interface[i].points for i in range(len(interface))]),
               show_edges=False,
               facecolor=(0.5, 0.5, 1.0),
               linecolor=(0, 0, 1.0))

viewer.show()

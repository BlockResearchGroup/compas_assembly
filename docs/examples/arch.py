from compas.geometry import Point, Line
from compas.datastructures import Mesh

from compas_assembly.datastructures import Block
from compas_assembly.datastructures import Assembly
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.geometry import Arch

from compas_view2.app import App
from compas_view2.objects import Object
from compas_view2.objects import MeshObject

# construct an arch assembly

arch = Arch(rise=5, span=10, thickness=0.7, depth=0.5, n=40)
assembly = Assembly.from_geometry(arch)

# define the boundary conditions

assembly.node_attribute(0, "is_support", True)
assembly.node_attribute(39, "is_support", True)

# identify the interfaces

assembly_interfaces(assembly)

# ==============================================================================
# Visualisation
# ==============================================================================

Object.register(Block, MeshObject)

viewer = App()

for node in assembly.nodes():
    point = Point(*assembly.node_attributes(node, "xyz"))
    block = assembly.node_attribute(node, "block")

    viewer.add(point, size=10, color=(0, 0, 0))

    viewer.add(
        block,
        show_faces=assembly.node_attribute(node, "is_support"),
        show_edges=True,
        facecolor=(1.0, 0, 0),
    )

for edge in assembly.edges():
    line = Line(*assembly.edge_coordinates(*edge))
    interface = assembly.edge_attribute(edge, "interface")

    viewer.add(line, linewidth=3, color=(0, 0.7, 0))

    viewer.add(
        Mesh.from_polygons([interface.points]),
        show_edges=False,
        facecolor=(0.5, 0.5, 1.0),
        linecolor=(0, 0, 1.0),
    )

viewer.show()

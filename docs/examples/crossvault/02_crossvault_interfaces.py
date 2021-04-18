import os
import compas

from compas.geometry import Point, Line, Polygon
from compas.datastructures import Mesh

from compas_assembly.datastructures import Assembly, Block
from compas_assembly.datastructures import assembly_interfaces_numpy

from compas_view2.app import App
from compas_view2.objects import Object, NetworkObject, MeshObject
from compas_view2.objects import Collection

Object.register(Assembly, NetworkObject)
Object.register(Block, MeshObject)


FILE_I = os.path.join(os.path.dirname(__file__), 'crossvault_assembly.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'crossvault_interfaces.json')

# ==============================================================================
# Load assembly
# ==============================================================================

assembly = compas.json_load(FILE_I)

# ==============================================================================
# Identify interfaces
# ==============================================================================

assembly_interfaces_numpy(assembly, tmax=0.02)

# ==============================================================================
# Export
# ==============================================================================

compas.json_dump(assembly, FILE_O)

# ==============================================================================
# Viz
# ==============================================================================

viewer = App()

nodes = []
blocks = []
interfaces = []
interactions = []

for node in assembly.nodes():
    nodes.append(Point(* assembly.node_coordinates(node)))
    blocks.append(assembly.node_attribute(node, 'block'))

for edge in assembly.edges():
    interface = assembly.edge_attribute(edge, 'interface')
    polygon = Polygon(interface.points)
    interfaces.append(Mesh.from_polygons([polygon]))

for edge in assembly.edges():
    a = Point(* assembly.node_coordinates(edge[0]))
    b = Point(* assembly.node_coordinates(edge[1]))
    interactions.append(Line(a, b))

viewer.add(Collection(nodes))
viewer.add(Collection(blocks), show_faces=False, show_edges=True)
viewer.add(Collection(interfaces), show_edges=False, color=(0, 0, 1), opacity=0.5)
viewer.add(Collection(interactions))

viewer.run()

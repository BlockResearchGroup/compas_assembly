import os
import compas

from compas.geometry import Point, Polygon
from compas.datastructures import Mesh

from compas_assembly.datastructures import Assembly, Block
from compas_assembly.datastructures import assembly_interfaces_numpy

from compas_view2.app import App
from compas_view2.objects import Object, NetworkObject, MeshObject
from compas_view2.objects import Collection

Object.register(Assembly, NetworkObject)
Object.register(Block, MeshObject)


FILE_I = os.path.join(os.path.dirname(__file__), 'armadillo_assembly.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'armadillo_interfaces.json')

assembly = compas.json_load(FILE_I)

assembly_interfaces_numpy(assembly, tmax=0.02, amin=0.0001)

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

for node in assembly.nodes():
    nodes.append(Point(* assembly.node_coordinates(node)))
    blocks.append(assembly.node_attribute(node, 'block'))

for edge in assembly.edges():
    interface = assembly.edge_attribute(edge, 'interface')
    polygon = Polygon(interface.points)
    interfaces.append(Mesh.from_polygons([polygon]))

viewer.add(Collection(nodes))
viewer.add(Collection(blocks), show_faces=False, show_edges=True)
viewer.add(Collection(interfaces), show_edges=False)

viewer.run()

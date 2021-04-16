import os
import compas

from compas.geometry import Point, Polygon
from compas.datastructures import Mesh
from compas.utilities import i_to_red

from compas_assembly.datastructures import Assembly, Block

from compas_view2.app import App
from compas_view2.objects import Object, NetworkObject, MeshObject
from compas_view2.objects import Collection

Object.register(Assembly, NetworkObject)
Object.register(Block, MeshObject)


FILE_I = os.path.join(os.path.dirname(__file__), 'armadillo_assembly.json')

assembly = compas.json_load(FILE_I)

# ==============================================================================
# Flatness
# ==============================================================================

# sides = []

# for node in assembly.nodes():
#     block = assembly.node_attribute(node, 'block')
#     faces = sorted(block.faces(), key=lambda face: block.face_area(face))[:-2]

# ==============================================================================
# Export
# ==============================================================================

# ==============================================================================
# Viz
# ==============================================================================

viewer = App()

nodes = []
blocks = []
interfaces = []
sides = []
colors = []

for node in assembly.nodes():
    nodes.append(Point(* assembly.node_coordinates(node)))
    blocks.append(assembly.node_attribute(node, 'block'))

for node in assembly.nodes():
    block = assembly.node_attribute(node, 'block')
    faces = sorted(block.faces(), key=lambda face: block.face_area(face))[:-2]
    for face in faces:
        side = Polygon(block.face_coordinates(face))
        mesh = Mesh.from_polygons([side])
        sides.append(mesh)

for mesh in sides:
    face = list(mesh.faces())[0]
    dev = mesh.face_flatness(face)
    colors.append(i_to_red(dev, normalize=True))

viewer.add(Collection(blocks), show_faces=False, show_edges=True)
viewer.add(Collection(sides), colors=colors, show_edges=False)

viewer.run()

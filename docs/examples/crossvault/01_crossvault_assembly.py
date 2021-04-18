import os
import compas

from compas.geometry import Point
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

from compas_view2.app import App
from compas_view2.objects import Collection

FILE_I = os.path.join(os.path.dirname(__file__), 'crossvault_meshes.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'crossvault_assembly.json')

# ==============================================================================
# Load meshes
# ==============================================================================

meshes = compas.json_load(FILE_I)

# ==============================================================================
# Construct assembly
# ==============================================================================

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

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

for node in assembly.nodes():
    nodes.append(Point(* assembly.node_coordinates(node)))
    blocks.append(assembly.node_attribute(node, 'block'))

viewer.add(Collection(nodes))
viewer.add(Collection(blocks), show_faces=True, show_edges=True, facecolor=(0.8, 0.8, 0.8), linecolor=(0, 0, 0))

viewer.run()

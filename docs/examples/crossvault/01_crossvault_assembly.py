import os
import compas

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
# from compas_assembly.rhino import AssemblyArtist

FILE_I = os.path.join(os.path.dirname(__file__), 'crossvault_meshes.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'crossvault_assembly.json')

meshes = compas.json_load(FILE_I)

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

compas.json_dump(assembly, FILE_O)

# artist = AssemblyArtist(assembly, layer="Crossvault::Assembly")
# artist.clear_layer()

# artist.draw_nodes(color={key: (255, 0, 0) for key in assembly.nodes_where({'is_support': True})})
# artist.draw_blocks()

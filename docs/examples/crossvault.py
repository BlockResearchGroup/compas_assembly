import os
import compas
import compas_blender

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces_numpy
from compas_assembly.blender import AssemblyArtist

# load meshes

FILE = os.path.join(os.path.dirname(__file__), 'crossvault.json')
meshes = compas.json_load(FILE)

# construct assembly

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# identify interfaces

assembly_interfaces_numpy(assembly, tmax=0.02, amin=0.0001)

# ==============================================================================
# Visualization
# ==============================================================================

compas_blender.clear()

artist = AssemblyArtist(assembly)

artist.draw_nodes()
artist.draw_blocks()
artist.draw_edges()
artist.draw_interfaces()

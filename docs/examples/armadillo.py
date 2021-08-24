import os
import compas

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.rhino import AssemblyArtist

from compas.rpc import Proxy

# prepare proxy for RPC

proxy = Proxy('compas_assembly.datastructures')

# load meshes

FILE = os.path.join(os.path.dirname(__file__), 'armadillo.json')
meshes = compas.json_load(FILE)

# construct assembly

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# identify interfaces

assembly = proxy.assembly_interfaces_numpy(assembly, tmax=0.02, amin=0.0001)

# ==============================================================================
# Visualization
# ==============================================================================

artist = AssemblyArtist(assembly, layer="Armadillo")
artist.clear_layer()

artist.draw_nodes()
artist.draw_blocks()
artist.draw_edges()
artist.draw_interfaces()

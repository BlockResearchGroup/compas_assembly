import compas
import compas_assembly
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.rhino import RhinoAssemblyArtist

from compas.rpc import Proxy

# prepare proxy for RPC

proxy = Proxy('compas_assembly.datastructures')

# load meshes

meshes = compas.json_load(compas_assembly.get("armadillo.json"))

# construct assembly

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# identify interfaces

assembly = proxy.assembly_interfaces(assembly, tmax=0.02, amin=0.0001)

# ==============================================================================
# Visualization
# ==============================================================================

artist = RhinoAssemblyArtist(assembly, layer="Armadillo")
artist.clear_layer()

artist.draw_nodes()
artist.draw_blocks()
artist.draw_edges()
artist.draw_interfaces()

import compas_blender

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces_numpy
from compas_assembly.geometry import Arch
from compas_assembly.blender import AssemblyArtist

from compas_rbe.equilibrium import compute_interface_forces_cvx

# ==============================================================================
# Assembly
# ==============================================================================

rise = 5
span = 10
depth = 0.5
thickness = 0.7
n = 40

arch = Arch(rise, span, thickness, depth, n)
assembly = Assembly.from_geometry(arch)

assembly.node_attribute(0, 'is_support', True)
assembly.node_attribute(n - 1, 'is_support', True)

# ==============================================================================
# Identify the interfaces
# ==============================================================================

assembly_interfaces_numpy(assembly)

# ==============================================================================
# Compute interface forces
# ==============================================================================

compute_interface_forces_cvx(assembly, solver='CPLEX')

# ==============================================================================
# Visualize
# ==============================================================================

compas_blender.delete_all_objects()

artist = AssemblyArtist(assembly, layer="Assembly")

artist.draw_nodes()
artist.draw_edges()
artist.draw_blocks(show_faces=True, show_vertices=False, show_edges=False)
artist.draw_interfaces()
artist.draw_resultants(scale=0.1)

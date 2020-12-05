from random import randint

import bpy
import compas_blender

from compas_assembly.datastructures import Assembly
# from compas_assembly.datastructures import assembly_interfaces_numpy
from compas_assembly.geometry import Arch
from compas_assembly.blender import AssemblyArtist

# from compas_rbe.equilibrium import compute_interface_forces_cvxopt

# ==============================================================================
# Assembly
# ==============================================================================

rise = 5
span = 10
depth = 0.5
thickness = 0.7
n = 15

arch = Arch(rise, span, thickness, depth, n)
assembly = Assembly.from_geometry(arch)

# assembly.node_attribute(0, 'is_support', True)
# assembly.node_attribute(n - 1, 'is_support', True)

# ==============================================================================
# Identify the interfaces
# ==============================================================================

# assembly_interfaces_numpy(assembly, tmax=0.1, amin=0.1)

# ==============================================================================
# Compute interface forces
# ==============================================================================

# compute_interface_forces_cvxopt(assembly)

# ==============================================================================
# Visualize
# ==============================================================================

compas_blender.clear()

artist = AssemblyArtist(assembly)

artist.draw_nodes()
# artist.draw_edges()
artist.draw_blocks()
# artist.draw_interfaces()
# artist.draw_resultants(0.05)

bpy.ops.object.select_all(action='DESELECT')

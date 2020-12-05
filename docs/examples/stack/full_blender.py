from random import choice

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import midpoint_point_point
from compas.geometry import transform_points
from compas.utilities import pairwise

import compas_blender

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces_numpy
from compas_assembly.blender import AssemblyArtist

from compas_rbe.equilibrium import compute_interface_forces_cvx


def shift(block):
    """Shift a block along the X or Y axis by a randomly chosen amount.

    Parameters
    ----------
    block : compas_assembly.datastructures.Block
    """
    scale = choice([+0.05, -0.05, +0.1, -0.1])
    axis = choice([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    vector = scale_vector(axis, scale)
    T = Translation(vector)
    block.transform(T)


# ==============================================================================
# Parameters
# ==============================================================================

# number of blocks

N = 10

# block dimensions

W = 2.0
H = 0.5
D = 1.0

# ==============================================================================
# Assembly
# ==============================================================================

assembly = Assembly()

# default block

box = Box.from_width_height_depth(W, H, D)
brick = Block.from_shape(box)

# make all blocks
# place each block on top of previous
# shift block randomly in XY plane

for i in range(N):
    block = brick.copy()
    block.transform(Translation([0, 0, 0.5 * H + i * H]))
    shift(block)
    assembly.add_block(block)

# mark the bottom block as support

assembly.node_attribute(0, 'is_support', True)

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
artist.draw_blocks()
artist.draw_interfaces()

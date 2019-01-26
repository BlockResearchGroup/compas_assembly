from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import choice

import compas_assembly

from compas.geometry import centroid_points_xy
from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Scale
from compas.geometry import subtract_vectors

from compas.datastructures import mesh_transform
from compas.datastructures import mesh_unify_cycles

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import identify_interfaces

from compas_assembly.viewer import AssemblyViewer

# number of blocks
N = 30

# block dimensions
W = 2.0
H = 0.5
D = 1.0

# empty assembly
assembly = Assembly()

# default block
box = Box.from_width_height_depth(W, H, D)
brick = Block.from_vertices_and_faces(box.vertices, box.faces)
mesh_unify_cycles(brick)

# make support block
box = Box.from_width_height_depth(W, 0.01, D)
support = Block.from_vertices_and_faces(box.vertices, box.faces)
mesh_unify_cycles(support)
S = Scale([1.2, 1.2, 1.0])
T = Translation([0, 0, -0.01])
M = T.concatenate(S)
mesh_transform(support, M)

# add support to assembly
assembly.add_block(support, is_support=True)

# make other blocks
# place each block on top of previous
# shift block randomly in XY plane
for i in range(N):
    block = brick.copy()
    factor = choice([+0.1, -0.1])
    T = Translation([factor * W, factor * H, i * H])
    mesh_transform(block, T)
    assembly.add_block(block)

# identify interfaces
identify_interfaces(assembly)

# find identifier of support
# and the first real block
key = list(assembly.vertices_where({'is_support': True}))[0]
nbr = assembly.vertex_neighbors(key)[0]

# translation vector
# for centring support and first block
a = centroid_points_xy(assembly.blocks[key].get_vertices_attributes('xyz'))
b = centroid_points_xy(assembly.blocks[nbr].get_vertices_attributes('xyz'))
ab = subtract_vectors(b, a)

# translate support
mesh_transform(support, Translation(ab))

# update interfaces
# (replace by more specifc function)
identify_interfaces(assembly)

# export to json
assembly.to_json(compas_assembly.get('stack.json'))

# # visualise the result
# viewer = AssemblyViewer()
# viewer.assembly = assembly
# viewer.show()

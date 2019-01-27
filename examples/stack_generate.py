"""Generate a stack of blocks.

1. Define the number of blocks and the block dimensions
2. Create an empty assembly.
3. Make a standard brick.
4. Add a support.
5. Add the blocks of the stack.
6. Identify the interfaces.
7. Find the first block above the support.
8. Centre the support to the first block.
9. Update the interfaces.
10. Serialise to json.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import choice

import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import scale_vector
from compas.geometry import add_vectors

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

# number of blocks
N = 10

# block dimensions
W = 2.0
H = 0.5
D = 1.0

# empty assembly
assembly = Assembly()

# default block
box = Box.from_width_height_depth(W, H, D)
brick = Block.from_vertices_and_faces(box.vertices, box.faces)

# make all blocks
# place each block on top of previous
# shift block randomly in XY plane
for i in range(N):
    block = brick.copy()
    factor = choice([+0.01, -0.01, +0.05, -0.05, +0.1, -0.1])
    axis = choice([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    vector = add_vectors(scale_vector(axis, factor), [0.0, 0.0, i * H])
    T = Translation(vector)
    mesh_transform(block, T)
    assembly.add_block(block)

# export to json
assembly.to_json(compas_assembly.get('assembly.json'))

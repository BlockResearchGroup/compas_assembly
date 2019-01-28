"""Generate a stack of blocks.

1. Define the number of blocks and the block dimensions
2. Create an empty assembly.
3. Make a standard brick.
5. Add the blocks of the stack.
6. Serialise to json.
7. Visualise the result

"""
from math import pi
from random import choice

import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import scale_vector
from compas.geometry import add_vectors

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_transform

from compas_assembly.plotter import AssemblyPlotter


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

    mesh_transform(block, Translation(vector))

    if i == 0:
        assembly.add_block(block, is_support=True)
    else:
        assembly.add_block(block)

# export to json

assembly.to_json(compas_assembly.get('stack.json'))

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, tight=True)

plotter.draw_vertices(text={key: str(key) for key, attr in assembly.vertices(True)})
plotter.draw_blocks(
    facecolor={key: '#ff0000' for key in assembly.vertices_where({'is_support': True})}
)
plotter.show()

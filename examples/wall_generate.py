from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Scale

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

# number of bricks in base course
number_of_bricks = 5

# number of courses
number_of_courses = 7

# brick dimensions
width = 2.0
height = 0.5
depth = 1.0

# horizontal joints
gap = 0.1

# brick geometry
box = Box.from_width_height_depth(width, height, depth)
brick = Block.from_vertices_and_faces(box.vertices, box.faces)

halfbrick = brick.copy()
S = Scale([(0.5 * (width - gap)) / width, 1.0, 1.0])
mesh_transform(halfbrick, S)

# empty assembly
wall = Assembly()

# add bricks in a staggered pattern
for i in range(number_of_courses):
    dy = i * height

    if i % 2 == 0:
        # in the even rows
        # add only full bricks

        for j in range(number_of_bricks):
            # make a copy of the base brick
            block = brick.copy()
            # move it to the right location
            T = Translation([j * (width + gap), 0, dy])
            mesh_transform(block, T)
            # add it to the assembly
            wall.add_block(block)
    else:
        # in the uneven rows
        # add a half brick + (number_of_bricks - 1) full bricks + a half brick

        # copy the base halfbrick
        block = halfbrick.copy()
        # move it to the right location
        T = Translation([0, 0, dy])
        mesh_transform(block, T)
        # add it to the assembly
        wall.add_block(block)

        for j in range(number_of_bricks - 1):
            # make a copy of the base brick
            block = brick.copy()
            # move it to the right location
            T = Translation([(0.5 + j) * (width + gap), 0, dy])
            mesh_transform(block, T)
            # add it ti=o the assembly
            wall.add_block(block)

        # copy the base halfbrick
        block = halfbrick.copy()
        # move it to the right location
        T = Translation([(0.5 + j + 1) * (width + gap), 0, dy])
        mesh_transform(block, T)
        # add it to the assembly
        wall.add_block(block)

# export to json
wall.to_json(compas_assembly.get('wall.json'))

"""Generate an assembly describing a brick wall.

Parameters
----------
number_of_even_bricks : int
    The number of bricks on the even rows.
number_of_courses : int
    The number of course rows in the wall.
width : float
    The width of the base brick.
height : float
    The height of the base brick.
depth : float
    The depth of the base brick.
gap : float
    The horizontal gap between the bricks.

Notes
-----
The script below does the same as ``compas_assembly.datastructures.assembly_from_wall()``.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

# number of bricks in base course
number_of_even_bricks = 5

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

# halfbrick geometry
box = Box.from_width_height_depth(0.5 * (width - gap), height, depth)
halfbrick = Block.from_vertices_and_faces(box.vertices, box.faces)

# empty assembly
assembly = Assembly()

# add bricks in a staggered pattern
for i in range(number_of_courses):
    dy = i * height

    if i % 2 == 0:
        # in the even rows
        # add (number_of_even_bricks) full bricks

        for j in range(number_of_even_bricks):
            # make a copy of the base brick
            block = brick.copy()
            # move it to the right location
            mesh_transform(block, Translation([j * (width + gap), 0, dy]))
            # add it to the assembly
            assembly.add_block(block)
    else:
        # in the uneven rows
        # add a half brick
        # add (number_of_even_bricks - 1) full bricks
        # add a half brick

        # copy the base halfbrick
        block = halfbrick.copy()
        # move it to the right location
        mesh_transform(block, Translation([0, 0, dy]))
        # add it to the assembly
        assembly.add_block(block)

        for j in range(number_of_even_bricks - 1):
            # make a copy of the base brick
            block = brick.copy()
            # move it to the right location
            mesh_transform(block, Translation([(0.5 + j) * (width + gap), 0, dy]))
            # add it ti=o the assembly
            assembly.add_block(block)

        # copy the base halfbrick
        block = halfbrick.copy()
        # move it to the right location
        mesh_transform(block, Translation([(0.5 + j + 1) * (width + gap), 0, dy]))
        # add it to the assembly
        assembly.add_block(block)

# export to json
assembly.to_json(compas_assembly.get('assembly.json'))

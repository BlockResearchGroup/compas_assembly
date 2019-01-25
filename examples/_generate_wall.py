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

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import identify_interfaces

from compas_assembly.viewer import AssemblyViewer

# number of bricks in base row
number_of_bricks = 5
number_of_courses = 7

# brick dimensions
width = 2.0
height = 0.5
depth = 1.0
gap = 0.1

# brick geometry
brick = Box.from_width_height_depth(width, height, depth)

# empty assembly
assembly = Assembly()

# add bricks in a staggered pattern
for i in range(number_of_courses):
    if i % 2 == 0:
        for j in range(number_of_bricks):
            block = Block.from_vertices_and_faces(brick.vertices, brick.faces)
            mesh_transform(block, Translation([j * (width + gap), 0, i * height]))
            assembly.add_block(block)
    else:
        for j in range(number_of_bricks - 1):
            block = Block.from_vertices_and_faces(brick.vertices, brick.faces)
            mesh_transform(block, Translation([0.5 * width + gap + j * (width + gap), 0, i * height]))
            assembly.add_block(block)

# export to json
assembly.to_json(compas_assembly.get('wall.json'))

# visualise the result
viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()

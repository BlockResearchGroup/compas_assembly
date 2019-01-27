from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Scale

from compas.datastructures import mesh_transform
from compas.datastructures import mesh_unify_cycles

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import identify_interfaces

from compas_assembly.viewer import AssemblyViewer

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
mesh_unify_cycles(brick)

# empty assembly
assembly = Assembly()

# add bricks in a staggered pattern
dy = 0
for i in range(number_of_courses):
    dx = 0
    if i % 2 == 0:
        # in the even rows we have only full bricks

        for j in range(number_of_bricks):
            block = brick.copy()
            T = Translation([dx, 0, dy])
            mesh_transform(block, T)
            assembly.add_block(block, is_support=(i == 0))
            dx += width + gap
    else:
        # in the uneven rows we have
        # a half brick + (number_of_bricks - 1) full bricks + another half brick

        # block = brick.copy()
        # S = Scale([(0.5 * (width - gap)) / width, 1.0, 1.0])
        # T = Translation([dx, 0, dy])
        # M = T.concatenate(S)
        # mesh_transform(block, M)
        # assembly.add_block(block)
        dx += 0.5 * (width + gap)

        for j in range(number_of_bricks - 1):
            block = brick.copy()
            mesh_transform(block, Translation([dx, 0, dy]))
            assembly.add_block(block)
            dx += width + gap

        # block = brick.copy()
        # S = Scale([(0.5 * (width - gap)) / width, 1.0, 1.0])
        # T = Translation([dx, 0, dy])
        # M = T.concatenate(S)
        # mesh_transform(block, M)
        # assembly.add_block(block)

    dy += height


# # identify interfaces
# identify_interfaces(assembly)

# export to json
assembly.to_json(compas_assembly.get('wall.json'))

# visualise the result
viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()

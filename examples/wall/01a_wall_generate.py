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

"""
import os

from compas.geometry import Box
from compas.geometry import Translation
from compas.datastructures import mesh_transform
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE = os.path.join(DATA, 'wall.json')


# number of bricks in even courses

number_of_even_bricks = 5

# number of courses

number_of_courses = 7

# brick dimensions

width = 1.0
height = 0.25
depth = 0.5

# horizontal joints

gap = 0.025

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
    dy = (0.5 + i) * height

    if i % 2 == 0:
        # in the even rows
        # add (number_of_even_bricks) full bricks

        for j in range(number_of_even_bricks):
            dx = 0.5 * width + j * (width + gap)
            T = Translation([dx, 0, dy])
            block = brick.copy()
            block.transform(T)
            assembly.add_block(block)
    else:
        # in the uneven rows
        # add a half brick
        # add (number_of_even_bricks - 1) full bricks
        # add a half brick

        dx = 0.25 * (width - gap)
        T = Translation([dx, 0, dy])
        block = halfbrick.copy()
        block.transform(T)
        assembly.add_block(block)

        for j in range(number_of_even_bricks - 1):
            dx = 0.5 * width + (0.5 + j) * (width + gap)
            T = Translation([dx, 0, dy])
            block = brick.copy()
            block.transform(T)
            assembly.add_block(block)

        dx = 0.25 * (width - gap) + (0.5 + j + 1) * (width + gap)
        T = Translation([dx, 0, dy])
        block = halfbrick.copy()
        block.transform(T)
        assembly.add_block(block)

# export to json

assembly.to_json(FILE)

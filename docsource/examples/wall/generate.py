import os
from math import pi

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.datastructures import mesh_transform
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.plotter import AssemblyPlotter


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE = os.path.join(DATA, 'wall.json')


# ==============================================================================
# Parameters
# ==============================================================================

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

# ==============================================================================
# Elements
# ==============================================================================

# brick geometry

box = Box.from_width_height_depth(width, height, depth)
brick = Block.from_shape(box)

# halfbrick geometry

box = Box.from_width_height_depth(0.5 * (width - gap), height, depth)
halfbrick = Block.from_shape(box)

# ==============================================================================
# Assembly
# ==============================================================================

assembly = Assembly()

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
        # add a half brick
        dx = 0.25 * (width - gap)
        T = Translation([dx, 0, dy])
        block = halfbrick.copy()
        block.transform(T)
        assembly.add_block(block)

        # add (number_of_even_bricks - 1) full bricks
        for j in range(number_of_even_bricks - 1):
            dx = 0.5 * width + (0.5 + j) * (width + gap)
            T = Translation([dx, 0, dy])
            block = brick.copy()
            block.transform(T)
            assembly.add_block(block)

        # add a half brick
        dx = 0.25 * (width - gap) + (0.5 + j + 1) * (width + gap)
        T = Translation([dx, 0, dy])
        block = halfbrick.copy()
        block.transform(T)
        assembly.add_block(block)

assembly.nodes_attribute('is_support', True, keys=list(range(number_of_even_bricks)))

# ==============================================================================
# Export
# ==============================================================================

assembly.to_json(FILE)

# ==============================================================================
# Visualize
# ==============================================================================

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly.transform(R)

plotter = AssemblyPlotter(assembly, figsize=(16, 10), tight=True)
plotter.draw_nodes(radius=0.02, facecolor={key: "#ff0000" for key in assembly.nodes_where({'is_support': True})})
plotter.draw_edges()
plotter.draw_blocks(edgecolor='#444444', edgewidth=0.5)
plotter.show()

import os
from math import pi

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.plotter import AssemblyPlotter
from compas_rhino.artists import MeshArtist


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE)
FILE = os.path.join(DATA, 'wall_test1.json')


def from_height_length_courses_and_nblocks(height, length, thickness, shifting, number_of_courses, number_of_blocks):
    """Create a masonry wall from its height, length, thickness, number of courses and number of blocks per row.

        Parameters
        ----------
        height : float
            Height of the wall.
        length : float
            length of the wall.
        thickness : float
            thickness of the wall.
        shifting : float between 0.0 and 0.99
            The shifting between blocks in two consecutive courses.
            if == 0: no shifting, the vertical joints in the wall are aligned.
        number_of_courses: int
            number of horizontal courses in the wall. 
        number_of_blocks: int
            number of blocks in one horizontal course of the wall. 

        Returns
        -------
        assembly of the masonry wall

"""
    assembly = Assembly()
    blocks = []
    block_h = height / number_of_courses
    block_l = length / number_of_blocks
    box = Box.from_width_height_depth(block_l, block_h, thickness)
    brick = Block.from_vertices_and_faces(box.vertices, box.faces)

    if shifting == 0:
        # full blocks in all courses (aligned joints)
        for i in range(number_of_courses):
            for j in range(number_of_blocks):
                dx = block_l * j
                dz = block_h * i
                T = Translation([dx, 0, dz])
                block = brick.copy()
                block.transform(T)
                blocks.append(block)
                assembly.add_block(block)

    else:
        # generation of the small block at the start of the odd courses
        small_block_l = block_l * shifting
        small_box = Box.from_width_height_depth(small_block_l, block_h, thickness)
        small_block = Block.from_vertices_and_faces(small_box.vertices, small_box.faces)
        # generation of the small block at the end of the odd courses
        small_block2_l = block_l - (block_l * shifting)
        small_box2 = Box.from_width_height_depth(small_block2_l, block_h, thickness)
        small_block2 = Block.from_vertices_and_faces(small_box2.vertices, small_box2.faces)

        for i in range(number_of_courses):
            if i % 2 == 0:
                # add full blocks in even courses
                for j in range(number_of_blocks):
                    dx = block_l * j
                    dz = block_h * i
                    T = Translation([dx, 0, dz])
                    block = brick.copy()
                    block.transform(T)
                    blocks.append(block)
                    assembly.add_block(block)
            else:
                # add the small block at the start of the odd courses
                dx = (block_l * 0.5) - (small_block_l * 0.5)
                dz = block_h * i
                T = Translation([-dx, 0, dz])
                block = small_block.copy()
                block.transform(T)
                blocks.append(block)
                assembly.add_block(block)
                # add full blocks in odd courses between start and end blocks
                for j in range(number_of_blocks - 1):
                    dx = small_block_l + block_l * j
                    dz = block_h * i
                    T = Translation([dx, 0, dz])
                    block = brick.copy()
                    block.transform(T)
                    blocks.append(block)
                    assembly.add_block(block)
                # add the small block at the end of the odd courses
                dx = small_block_l + (block_l * (number_of_blocks - 2)) + block_l / 2 + small_block2_l / 2
                dz = block_h * i
                T = Translation([dx, 0, dz])
                block = small_block2.copy()
                block.transform(T)
                blocks.append(block)
                assembly.add_block(block)

    # Supports
    assembly.nodes_attribute('is_support', True, keys=list(range(number_of_blocks)))

    return blocks, assembly


def from_height_length_and_block_size(height, length, thickness, shifting, block_h, block_l):
    """Create a masonry wall from its height, length, thickness, and the dimensions (height and length) of a block.

    This function is especially useful after a survey on-site, where the overall dimensions of the wall and the average
    block size are taken. This function will slightly change the block's dimensions to precisely populate the wall keeping fixed
    its overall dimensions.

        Parameters
        ----------
        height : float
            Height of the wall.
        length : float
            length of the wall.
        thickness : float
            thickness of the wall.
        shifting : float between 0.0 and 0.99
            The shifting between blocks in two consecutive courses.
            if == 0: no shifting, the vertical joints in the wall are aligned.
        block_h: float
            height of a block. 
        block_l: float
            length of a block. 

        Returns
        -------
        assembly of the masonry wall

"""
    assembly = Assembly()
    blocks = []

    ratio_h = height / block_h
    ratio_l = length / block_l

    final_block_h = height / int(ratio_h)
    final_block_l = length / int(ratio_l)

    n_courses = int(ratio_h)
    n_blocks = int(ratio_l)

    box = Box.from_width_height_depth(final_block_l, final_block_h, thickness)
    brick = Block.from_vertices_and_faces(box.vertices, box.faces)

    if shifting == 0:
        # full blocks in all courses (aligned joints)
        for i in range(n_courses):
            for j in range(n_blocks):
                dx = final_block_l * j
                dz = final_block_h * i
                T = Translation([dx, 0, dz])
                block = brick.copy()
                block.transform(T)
                blocks.append(block)
                assembly.add_block(block)

    else:
        # generation of the small block at the start of the odd courses
        small_block_l = final_block_l * shifting
        small_box = Box.from_width_height_depth(small_block_l, final_block_h, thickness)
        small_block = Block.from_vertices_and_faces(small_box.vertices, small_box.faces)

        small_block2_l = final_block_l - (final_block_l * shifting)
        small_box2 = Box.from_width_height_depth(small_block2_l, final_block_h, thickness)
        small_block2 = Block.from_vertices_and_faces(small_box2.vertices, small_box2.faces)

        for i in range(n_courses):
            if i % 2 == 0:
                # add full blocks in even courses
                for j in range(n_blocks):
                    dx = final_block_l * j
                    dz = final_block_h * i
                    T = Translation([dx, 0, dz])
                    block = brick.copy()
                    block.transform(T)
                    blocks.append(block)
                    assembly.add_block(block)
            else:
                # add the small block at the start of the odd courses
                dx = (final_block_l * 0.5) - (small_block_l * 0.5)
                dz = final_block_h * i
                T = Translation([-dx, 0, dz])
                block = small_block.copy()
                block.transform(T)
                blocks.append(block)
                assembly.add_block(block)
                # add full blocks in odd courses between start and end blocks
                for j in range(n_blocks - 1):
                    dx = small_block_l + final_block_l * j
                    dz = final_block_h * i
                    T = Translation([dx, 0, dz])
                    block = brick.copy()
                    block.transform(T)
                    blocks.append(block)
                    assembly.add_block(block)
                # add the small block at the end of the odd courses
                dx = small_block_l + (final_block_l * (n_blocks - 2)) + final_block_l / 2 + small_block2_l / 2
                dz = final_block_h * i
                T = Translation([dx, 0, dz])
                block = small_block2.copy()
                block.transform(T)
                blocks.append(block)
                assembly.add_block(block)

    # Supports
    assembly.nodes_attribute('is_support', True, keys=list(range(n_blocks)))

    return blocks, assembly


# ==============================================================================
# Parameters
# ==============================================================================
height = 4.0
length = 8.0
thickness = 0.3
shifting = 0.5
number_of_courses = 20
number_of_blocks = 10
block_h = 0.2
block_l = 0.6

# function1
# ==============================================================================
blocks, assembly = from_height_length_courses_and_nblocks(
    height, length, thickness, shifting, number_of_courses, number_of_blocks)

# function2
# ==============================================================================
# blocks, assembly = from_height_length_and_block_size(
#     height, length, thickness, shifting, block_h, block_l)


# ==============================================================================
# Export
# ==============================================================================

assembly.to_json(FILE)


# ==============================================================================
# Visualize
# ==============================================================================

# Blocks in Rhino
# ==============================================================================

# for b in blocks:
#     artist = MeshArtist(b)
#     artist.draw_mesh()


# Assembly in plotter
# ==============================================================================

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly.transform(R)
plotter = AssemblyPlotter(assembly, figsize=(16, 10), tight=True)
plotter.draw_nodes(radius=0.02, facecolor={key: "#ff0000" for key in assembly.nodes_where({'is_support': True})})
plotter.draw_edges()
plotter.draw_blocks(edgecolor='#444444', edgewidth=0.5)
plotter.show()

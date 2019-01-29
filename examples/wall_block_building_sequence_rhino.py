""""""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence

from compas_assembly.rhino import AssemblyArtist
from compas_assembly.rhino import AssemblyHelper


# just so Rhino(Mac) gets the filepaths right

HERE = os.path.dirname(__file__)

# load an assembly from a JSON file

assembly = Assembly.from_json(os.path.join(HERE, '../data/wall_courses.json'))

# make a list of the blocks that were already placed

placed = list(assembly.vertices_where({'is_placed': True}))

# draw the assembly

artist = AssemblyArtist(assembly, layer="Assembly")

artist.clear_layer()
artist.draw_vertices()
artist.draw_blocks(show_faces=False, show_edges=True)

# draw filled in blocks for the placed ones

if placed:
    artist.draw_blocks(keys=placed, show_faces=True, show_edges=False)

# make sure Rhino redraws the view

artist.redraw()

# select a block

key = AssemblyHelper.select_vertex(assembly)

# exit if none was selected

if key is None:
    raise Exception("No block was selected.")

# get the sequence

sequence = assembly_block_building_sequence(assembly, key)
print(sequence)

# draw the blocks of the sequence

if sequence:
    keys = list(set(sequence) - set(placed))
    artist.draw_blocks(keys=keys, show_faces=True, show_edges=False)
    artist.redraw()

"""

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.rhino import AssemblyArtist
from compas_assembly.rhino import AssemblyHelper


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')

assembly = Assembly.from_json(os.path.join(DATA, 'assembly.json'))

# selected block

artist = AssemblyArtist(assembly, layer="Assembly")
artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.draw_blocks()
artist.draw_interfaces()
artist.redraw()

placed = list(assembly.vertices_where({'is_placed': True}))
artist.draw_blocks(keys=placed, show_faces=True, show_edges=False)

placed = set(placed)

sequence = []

while True:
    # select the block you want to place
    key = AssemblyHelper.select_vertex(assembly)

    if key is None:
        print('Nothing selected.')
        break

    # which neighbour have already been placed
    # could be based on course information

    nbrs = assembly.vertex_neighbors(key)

    if not nbrs:
        raise Exception('The selected block has no neighbors.\nPerhaps the interfaces have not been identified.')

    placed_nbrs = list(set(nbrs) & placed)

    if not placed_nbrs:
        print('This block cannot be placed.')
        continue

    placed.add(key)

    sequence.append(key)

    artist.draw_blocks(keys=[key], show_faces=True, show_edges=False)
    artist.redraw()


if sequence:
    pass

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

while True:
    # select the block you want to place
    key = AssemblyHelper.select_vertex(assembly)

    if key is None:
        break

    # which neighbour have already been placed
    # could be based on course information

    nbrs = assembly.vertex_neighbors(key)

    if not nbrs:
        raise Exception('The selected block has no neighbors.\nPerhaps the interfaces have not been identified.')

    supports = []
    for nbr in nbrs:
        if assembly.get_vertex_attribute(nbr, 'is_placed'):
            supports.append(nbr)

    if not supports:
        print('This block cannot be placed.')
        continue

    # evaluate equilibrium of subset of the assembly

    # block = assembly.blocks[key]
    # # "top" face frame
    # frames = block.frames()
    # fkey, frame = sorted(frames.items(), key=lambda x: x[1][0][2])[-1]
    # print(key, fkey, frame)

    artist.draw_blocks(supports, show_faces=True, show_edges=False)

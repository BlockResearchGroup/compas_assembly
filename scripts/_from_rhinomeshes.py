from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas_rhino

from compas_assembly.datastructures import Assembly
from compas_assembly.rhino import AssemblyHelper


HERE = os.path.abspath(os.path.dirname(__file__))


drawsettings = {
    'show.vertices': True,
    'layer': 'Assembly',
}


wall = Assembly()

guids = compas_rhino.select_surfaces()
wall.add_blocks_from_polysurfaces(guids)

wall.draw(drawsettings)

while True:
    keys = AssemblyHelper.select_vertices(wall)
    if not keys:
        break

    if AssemblyHelper.update_vertex_attributes(wall, keys):
        wall.draw(drawsettings)


wall.to_json(os.path.join(HERE, '../data/frompolysurfaces.json'))

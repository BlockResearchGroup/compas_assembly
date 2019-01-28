"""Add a support plate to an assembly and identify the interfaces.

1. ...

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas.geometry import bounding_box_xy
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import subtract_vectors
from compas.geometry import length_vector

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces


assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

points = []
for key in assembly.vertices():
    block = assembly.blocks[key]
    xyz = block.get_vertices_attributes('xyz')
    points.extend(xyz)

bbox = bounding_box_xy(points)
support = Block.from_vertices_and_faces(bbox, [[0, 1, 2, 3]])

c0 = support.centroid()

lx = length_vector(subtract_vectors(bbox[1], bbox[0]))
ly = length_vector(subtract_vectors(bbox[2], bbox[1]))
sx = (0.5 + lx) / lx
sy = (0.5 + ly) / ly

S = Scale([sx, sy, 1.0])
mesh_transform(support, S)

c1 = support.centroid()

T = Translation(subtract_vectors(c0, c1))
mesh_transform(support, T)

assembly.add_block(support, is_support=True, is_placed=True)

assembly_interfaces(assembly, nmax=200)

assembly.to_json(compas_assembly.get('assembly.json'))

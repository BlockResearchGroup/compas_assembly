"""Add a support plate to a wll assembly and identify the interfaces.

1. Load an assembly from a json file
2. Compute the footprint of the assembly
3. Add a support in the XY plane at least the size to the footprint
4. Compute the interfaces of the assembly
5. Serialise the result

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
from compas.geometry import centroid_points

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces_numpy


# load assembly from JSON
assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

# list the coordinates of all vertices of all blocks
points = []
for key in assembly.vertices():
    block = assembly.blocks[key]
    xyz = block.get_vertices_attributes('xyz')
    points.extend(xyz)

# compute the XY bounding box of all listed vertices
bbox = bounding_box_xy(points)

# make a support block of the same size as the bounding box
support = Block.from_vertices_and_faces(bbox, [[0, 1, 2, 3]])

# scale the support
lx = length_vector(subtract_vectors(bbox[1], bbox[0]))
ly = length_vector(subtract_vectors(bbox[2], bbox[1]))
sx = (0.5 + lx) / lx
sy = (0.5 + ly) / ly

S = Scale([sx, sy, 1.0])
mesh_transform(support, S)

# align the centroid of the support with the centroid of the bounding box
c0 = centroid_points(bbox)
c1 = support.centroid()

T = Translation(subtract_vectors(c0, c1))
mesh_transform(support, T)

# add the support to the assembly
assembly.add_block(support, is_support=True, is_placed=True)

# identify the interfaces
assembly_interfaces_numpy(assembly, nmax=200)

# serialise
assembly.to_json(compas_assembly.get('assembly_supported.json'))

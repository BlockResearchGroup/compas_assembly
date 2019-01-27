"""Add imperfections to a stack.

1. Load an assembly from a JSON file.
2. Make sure there are supports.
3. Identify the interfaces.
4.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import radians
from random import choice

import compas_assembly

from compas.datastructures import mesh_transform
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import scale_vector

from compas_assembly.datastructures import Assembly


XYZ = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
ANGLES = [radians(1), radians(-1), radians(2), radians(-2)]

assembly = Assembly.from_json(compas_assembly.get('stack.json'))

# shift and rotate in random directions
# use small increments ("imperfections")
# recompute the interfaces
for key in assembly.vertices():
    # replace this by a loop over the blocks?
    block = assembly.blocks[key]
    R = Rotation.from_axis_and_angle(choice(XYZ), choice(ANGLES), block.centroid())
    T = Translation(scale_vector(choice(XYZ), choice([0.01, -0.01])))
    mesh_transform(block, T.concatenate(R))

assembly.to_json(compas_assembly.get('stack_imperfections.json'))

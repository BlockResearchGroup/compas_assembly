"""Add imperfections to a stack.

1. Load an assembly from a JSON file.
2. Add a random imperfection to every block.
3. Serialise
4. Visualise

"""
from math import radians
from math import pi
from random import choice

import compas_assembly

from compas.datastructures import mesh_transform
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import scale_vector

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform

from compas_assembly.plotter import AssemblyPlotter


# possible imperfection

XYZ = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
ANGLES = [radians(1), radians(-1), radians(2), radians(-2)]

# load an assembly

assembly = Assembly.from_json(compas_assembly.get('stack.json'))

# shift and rotate in random directions
# use small increments ("imperfections")

for key in assembly.vertices():
    block = assembly.blocks[key]

    R = Rotation.from_axis_and_angle(choice(XYZ), choice(ANGLES), block.centroid())
    T = Translation(scale_vector(choice(XYZ), choice([0.01, -0.01])))

    mesh_transform(block, T.concatenate(R))

# serialise

assembly.to_json(compas_assembly.get('assembly.json'))

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, tight=True)

plotter.draw_vertices(text={key: str(key) for key, attr in assembly.vertices(True)})
plotter.draw_blocks(
    facecolor={key: '#ff0000' for key in assembly.vertices_where({'is_support': True})}
)
plotter.show()

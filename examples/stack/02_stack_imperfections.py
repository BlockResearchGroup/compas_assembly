"""Add imperfections to a stack.

1. Load an assembly from a JSON file.
2. Add a random imperfection to every block.
3. Serialise
4. Visualise

"""
import os
from math import radians
from math import pi
from random import choice
from compas.geometry import Rotation
from compas.geometry import Translation
from compas.geometry import scale_vector
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE_I = os.path.join(DATA, 'stack.json')
FILE_O = os.path.join(DATA, 'stack.json')


# possible imperfections

XYZ = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
ANGLES = [radians(0.5), radians(-0.5), radians(0.1), radians(-0.1)]

# load an assembly

assembly = Assembly.from_json(FILE_I)

# shift and rotate in random directions
# use small increments ("imperfections")

for key in assembly.nodes():
    block = assembly.blocks[key]

    R = Rotation.from_axis_and_angle(choice(XYZ), choice(ANGLES), block.centroid())
    T = Translation(scale_vector(choice(XYZ), choice([0.005, -0.005])))

    # block.transform(T.concatenated(R))
    block.transform(T * R)

# serialise

assembly.to_json(FILE_O)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(5, 8) ,tight=True)

plotter.draw_nodes(text={key: str(key) for key, attr in assembly.nodes(True)})
plotter.draw_blocks(
    facecolor={key: '#ff0000' for key in assembly.nodes_where({'is_support': True})})
plotter.show()

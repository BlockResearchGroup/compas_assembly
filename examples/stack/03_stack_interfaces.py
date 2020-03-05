"""Identify the interfaces of a stack.

1. Load a stack from a json file
2. Identify the interfaces
3. Export to json
4. Visualise

"""
import os
from math import pi
from compas.geometry import Rotation
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.datastructures import assembly_interfaces_numpy
from compas_assembly.plotter import AssemblyPlotter


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE_I = os.path.join(DATA, 'stack.json')
FILE_O = os.path.join(DATA, 'stack.json')


# load assembly

assembly = Assembly.from_json(FILE_I)

# identify_interfaces

assembly_interfaces_numpy(assembly, tmax=0.02)

# export to json

assembly.to_json(FILE_O)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(5, 8), tight=True)
plotter.draw_nodes(text='key')
plotter.draw_edges()
plotter.draw_blocks(facecolor={key: '#ff0000' for key in assembly.nodes_where({'is_support': True})})
plotter.show()

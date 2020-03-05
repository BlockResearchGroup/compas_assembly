import os
from math import pi
from compas.geometry import Rotation
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE = os.path.join(DATA, 'wall_supported.json')


assembly = Assembly.from_json(FILE)

# ==============================================================================
# Visuzalize
# ==============================================================================

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

supports = list(assembly.nodes_where({'is_support': True}))

edgecolor = {key: '#444444' for key in assembly.nodes()}
edgecolor.update({key: '#ff0000' for key in supports})

edgewidth = {key: 0.5 for key in assembly.nodes()}
edgewidth.update({key: 3.0 for key in supports})

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.draw_blocks(edgecolor=edgecolor, edgewidth=edgewidth)
plotter.show()

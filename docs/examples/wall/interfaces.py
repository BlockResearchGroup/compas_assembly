import os
from math import pi
from compas.geometry import Rotation
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces_numpy
from compas_assembly.plotter import AssemblyPlotter


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE_I = os.path.join(DATA, 'wall.json')
FILE_O = os.path.join(DATA, 'wall_interfaces.json')


# ==============================================================================
# Load assembly from file
# ==============================================================================

assembly = Assembly.from_json(FILE_I)

# ==============================================================================
# Identify interfaces
# ==============================================================================

assembly_interfaces_numpy(assembly, nmax=100, amin=0.0001)

# ==============================================================================
# Export
# ==============================================================================

assembly.to_json(FILE_O)

# ==============================================================================
# Visualize
# ==============================================================================

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly.transform(R)

plotter = AssemblyPlotter(assembly, figsize=(8, 5), tight=True)

plotter.draw_nodes(radius=0.02, facecolor={key: "#ff0000" for key in assembly.nodes_where({'is_support': True})})
plotter.draw_edges()
plotter.draw_blocks(edgecolor='#444444', edgewidth=0.5)
plotter.show()

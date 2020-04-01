import os
from math import pi
from compas_assembly.datastructures import Assembly
from compas_assembly.geometry import Arch
from compas_assembly.plotter import AssemblyPlotter
from compas.geometry import Rotation


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE = os.path.join(DATA, 'arch.json')

# ==============================================================================
# Assembly
# ==============================================================================

rise = 5
span = 10
thickness = 0.7
depth = 0.5
n = 40

arch = Arch(rise, span, thickness, depth, n)
assembly = Assembly.from_geometry(arch)

assembly.node_attribute(0, 'is_support', True)
assembly.node_attribute(n - 1, 'is_support', True)

# ==============================================================================
# Export
# ==============================================================================

assembly.to_json(FILE)

# ==============================================================================
# Visualize
# ==============================================================================

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2, [0, 0, 0])
assembly.transform(R)

plotter = AssemblyPlotter(assembly, figsize=(16, 10), tight=True)
plotter.draw_nodes(radius=0.05)
plotter.draw_edges()
plotter.draw_blocks(facecolor={key: '#ff0000' for key in assembly.nodes_where({'is_support': True})})
plotter.show()

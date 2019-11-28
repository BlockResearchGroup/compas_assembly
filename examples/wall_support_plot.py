from math import pi

from compas.geometry import Rotation

import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter

FILE = compas_assembly.get('wall_supported.json')

assembly = Assembly.from_json(FILE)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)

supports = list(assembly.vertices_where({'is_support': True}))

edgecolor = {key: '#444444' for key in assembly.vertices()}
edgecolor.update({key: '#ff0000' for key in supports})
edgewidth = {key: 0.5 for key in assembly.vertices()}
edgewidth.update({key: 3.0 for key in supports})

plotter.draw_blocks(edgecolor=edgecolor, edgewidth=edgewidth)
plotter.show()

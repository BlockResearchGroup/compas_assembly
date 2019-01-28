from math import pi

import compas_assembly

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.datastructures import assembly_construct_wall
from compas_assembly.plotter import AssemblyPlotter


assembly = Assembly.from_json(compas_assembly.get('wall.json'))

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.assembly_plotter.defaults['vertex.fontsize'] = 10

plotter.draw_vertices(
    text={key: str(key) for key in assembly.vertices()}
)
plotter.draw_blocks()
plotter.show()

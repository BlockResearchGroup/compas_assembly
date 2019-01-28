from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

from compas.geometry import Rotation

from compas_assembly.datastructures import assembly_transform
from compas_assembly.datastructures import assembly_from_wall
from compas_assembly.plotter import AssemblyPlotter


assembly = assembly_from_wall(5, 7, 2.0, 0.5, 1.0, 0.1)

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.assembly_plotter.defaults['vertex.fontsize'] = 10

plotter.draw_vertices(
    text={key: str(key) for key in assembly.vertices()}
)
plotter.draw_blocks_bbox()
plotter.show()

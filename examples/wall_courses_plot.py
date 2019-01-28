from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

import compas_assembly

from compas.utilities import i_to_red

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter


assembly = Assembly.from_json(compas_assembly.get('assembly_courses.json'))

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.assembly_plotter.defaults['vertex.fontsize'] = 10

courses = assembly.get_vertices_attribute('course')

c_min = min(courses)
c_max = max(courses)
c_spn = c_max - c_min

facecolor = {key: i_to_red((attr['course'] - c_min) / c_spn) for key, attr in assembly.vertices(True)}

plotter.draw_vertices(
    text={key: str(attr['course']) for key, attr in assembly.vertices(True)},
    facecolor=facecolor
)
plotter.draw_blocks_bbox()
plotter.show()

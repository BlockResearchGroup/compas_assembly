""""""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi
from random import choice

import compas_assembly

from compas.utilities import i_to_red

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_block_building_sequence
from compas_assembly.datastructures import assembly_transform

from compas_assembly.plotter import AssemblyPlotter


# load an assembly from a JSON file

assembly = Assembly.from_json(compas_assembly.get('assembly_courses.json'))

# get a random block from the top course

c_max = max(assembly.get_vertices_attribute('course'))
key = choice(list(assembly.vertices_where({'course': c_max})))

# get the sequence

sequence = assembly_block_building_sequence(assembly, key)
print(sequence)

# rotate the assembly for visualisation

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

# make a plotter

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.assembly_plotter.defaults['vertex.fontsize'] = 10

# color vertices according to their building order

i_min = 0
i_max = len(sequence)
i_spn = i_max - i_min

facecolor = {k: '#cccccc' for k in assembly.vertices()}
facecolor.update({k: i_to_red((index - i_min) / i_spn) for index, k in enumerate(sequence[::-1])})
facecolor[key] = '#ff0000'

# plot the assembly vertices

plotter.draw_vertices(
    text={key: str(key) for key in assembly.vertices()},
    facecolor=facecolor
)

# plot the block bounding boxes

plotter.draw_blocks_bbox()
plotter.show()

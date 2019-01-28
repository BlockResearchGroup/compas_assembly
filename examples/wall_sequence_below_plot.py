from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi
from random import choice
from collections import deque

import compas_assembly

from compas.utilities import i_to_red

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter


assembly = Assembly.from_json(compas_assembly.get('assembly_courses.json'))

key = choice(list(assembly.vertices_where({'course': 7})))
course = assembly.get_vertex_attribute(key, 'course')
block = assembly.blocks[key]

sequence = []
seen = set()
tovisit = deque([(key, course + 1)])

while tovisit:
    k, course_above = tovisit.popleft()

    if k not in seen:
        seen.add(k)

        course = assembly.get_vertex_attribute(k, 'course')

        if course_above == course + 1:
            sequence.append(k)

            for nbr in assembly.vertex_neighbors(k):
                if nbr not in seen:
                    tovisit.append((nbr, course))

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.assembly_plotter.defaults['vertex.fontsize'] = 10

i_min = 0
i_max = len(sequence)
i_spn = i_max - i_min

facecolor = {k: '#cccccc' for k in assembly.vertices()}
facecolor.update({k: i_to_red((index - i_min) / i_spn) for index, k in enumerate(sequence[::-1])})
facecolor[key] = '#ff0000'

plotter.draw_vertices(
    text={key: str(key) for key in assembly.vertices()},
    facecolor=facecolor
)
plotter.draw_blocks_bbox()
plotter.show()

"""Visualise information about the assembly in a plotter.

1. Load an assembly from a JSON file.
2. Set up a plotter
3. Plot vertex keys and red supports
4.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

import compas_assembly

from compas.datastructures import network_transform
from compas.datastructures import mesh_transform
from compas.geometry import Rotation
from compas.geometry import bounding_box_xy

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import identify_interfaces
from compas_assembly.plotter import AssemblyPlotter

# load an assembly from serialised data in a json file
assembly = Assembly.from_json(compas_assembly.get('stack_imperfections.json'))

# compute the interfaces between the blocks of the assembly
identify_interfaces(assembly, tmax=0.1)

# rotate the assembly to the XY plane
# note: replace this by assembly_transform and include the blocks in the transformation
# note: make obsolete by providing a viewing axis to the plotter
R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
network_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(10, 7))

plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in assembly.vertices_where({'is_support': True})},
    text={key: str(key) for key in assembly.vertices()})

plotter.draw_edges()

polylines = []
for key, attr in assembly.vertices(True):
    block = assembly.blocks[key]
    mesh_transform(block, R)
    box = bounding_box_xy(block.get_vertices_attributes('xyz'))
    polylines.append({
        'points': box + box[:1],
        'color': '#ff0000' if attr['is_support'] else '#cccccc',
    })
plotter.draw_polylines(polylines)

plotter.show()

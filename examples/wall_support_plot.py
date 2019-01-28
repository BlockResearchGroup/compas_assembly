from math import pi

import compas_assembly

from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_transform
from compas_assembly.plotter import AssemblyPlotter


assembly = Assembly.from_json(compas_assembly.get('wall_supported.json'))

# visualise

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly_transform(assembly, R)

plotter = AssemblyPlotter(assembly, figsize=(16, 6), tight=True)
plotter.assembly_plotter.defaults['vertex.fontsize'] = 10

supports = list(assembly.vertices_where({'is_support': True}))

color = {key: '#ff0000' for key in supports}

plotter.draw_vertices(
    text={key: str(key) for key in assembly.vertices()},
    facecolor=color,
)
plotter.draw_blocks(
    facecolor=color,
    edgecolor=color,
    edgewidth={key: 3 for key in supports}
)
plotter.show()

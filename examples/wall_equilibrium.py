from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi

import compas_assembly

from compas.plotters import NetworkPlotter

from compas.datastructures import network_transformed
from compas.geometry import Rotation

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import identify_interfaces

from compas_rbe.equilibrium import compute_interface_forces_cvx


assembly = Assembly.from_json(compas_assembly.get('wall.json'))

keys = list(assembly.vertices_where({'is_support': True}))
print(keys)

if keys:
    identify_interfaces(assembly)

    R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
    network = network_transformed(assembly, R)
    plotter = NetworkPlotter(network, figsize=(10, 7))
    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in network.vertices_where({'is_support': True})})
    plotter.draw_edges()
    plotter.show()

    compute_interface_forces_cvx(assembly, solver='CVXOPT', verbose=True)

    assembly.to_json(compas_assembly.get('wall_result.json'))

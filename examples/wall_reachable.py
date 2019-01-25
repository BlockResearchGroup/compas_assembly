from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas.geometry import distance_point_point
from compas.geometry import Frame

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import identify_interfaces


wall = Assembly.from_json(compas_assembly.get('frompolysurfaces.json'))

identify_interfaces(wall)

# robot location
# robot action radius

robot_base = Frame([0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
robot_radius = 3.0

# distance from robot base origin to each block
# blocks within radius

key_index = wall.key_index()

origin = robot_base.point
centroids = [wall.blocks[key].centroid() for key in wall.vertices()]

distances = [distance_point_point(origin, centroid) for centroid in centroids]

# reachable = []
# for key in wall.vertices():
#     index = key_index[key]
#     d = distances[index]
#     if d < robot_radius:
#         reachable.append(key)

# print(reachable)

print([key for key in wall.vertices() if distances[key_index[key]] < robot_radius])

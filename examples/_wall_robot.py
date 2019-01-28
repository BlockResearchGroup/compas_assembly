# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

# import compas_assembly

# from compas.utilities import flatten
# from compas.utilities import pairwise

# from compas.geometry import distance_point_point
# from compas.geometry import Frame
# from compas.geometry import Translation
# from compas.geometry import bounding_box
# from compas.geometry import oriented_bounding_box_numpy
# from compas.geometry import oriented_bounding_box_xy_numpy
# from compas.geometry import subtract_vectors
# from compas.geometry import length_vector

# # from compas.numerical import pca_numpy

# from compas_assembly.datastructures import Assembly
# from compas_assembly.datastructures import assembly_interfaces


# wall = Assembly.from_json(compas_assembly.get('assembly.json'))

# key_index = wall.key_index()

# points = list(flatten([wall.blocks[key].get_vertices_attributes('xyz') for key in wall.vertices()]))
# centroids = [wall.blocks[key].centroid() for key in wall.vertices()]

# # mean, axes, spread = pca_numpy(points)

# # print(mean)
# # print(list(zip(axes, spread)))

# box, area = oriented_bounding_box_xy_numpy(points)

# print(box)

# assembly_interfaces(wall)

# box = bounding_box(points)
# width = max(length_vector(subtract_vectors(b, a)) for a, b in pairwise(box))

# print(box)

# # robot_base = Frame([0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
# # robot_radius = 3.0

# # N = int(width // robot_radius)
# # L = width / N

# # for i in range(N + 1):


# #     origin = robot_base.point

# #     distances = [distance_point_point(origin, centroid) for centroid in centroids]
# #     reachable = [key for key in wall.vertices() if distances[key_index[key]] < robot_radius]

# #     print(reachable)

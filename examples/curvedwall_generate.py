"""Generate a wall assembly along a set of curves.

1. ...

Note
----
This example uses a very basic implementation of a Curve to define the geometry
of the assembly. Try reimplementing it based on a RhinoCurve object (``compas_rhino.geometry.RhinoCurve``)
in Rhino to improve the placement of blocks along the curve;
for example, without overlaps...

"""
import compas_assembly

from compas.geometry import Bezier
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import Box
from compas.geometry import cross_vectors

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block


# number of bricks in base course
number_of_bricks = 10

# number of courses
number_of_courses = 10

# brick dimensions
width = 2.0
height = 0.5
depth = 1.0

span = number_of_bricks * width
rise = 5.0

# create an empty assembly
assembly = Assembly()

# create a base brick
box = Box.from_width_height_depth(2.0, 0.5, 1.0)
brick = Block.from_vertices_and_faces(box.vertices, box.faces)

cx, cy, cz = brick.centroid()
v1 = [-cx, -cy, 0]

for i in range(number_of_courses):
    controls = [
        [0, 0, 0],
        [span / 3.0, -1.0 * (rise - i * rise / (number_of_courses - 1)), 0],
        [2 * span / 3.0, (rise - i * rise / (number_of_courses - 1)), 0],
        [span, 0, 0]
    ]
    curve = Bezier(controls)

    if i % 2 == 0:
        for j in range(0, number_of_bricks + 1):
            block = brick.copy()
            # move the brick to the right location
            # and align it with the local tangent
            t = j / number_of_bricks
            p = curve.compute_point(t)
            u = curve.compute_tangent(t)
            v = cross_vectors([0.0, 0.0, 1.0], u)
            T2 = Translation(p + [0, 0, i * height])
            R = Rotation.from_basis_vectors(u, v)
            T1 = Translation(v1)
            mesh_transform(block, T2.concatenate(R).concatenate(T1))
            # add the brick to the assembly
            assembly.add_block(block)
    else:
        for j in range(0, number_of_bricks):
            block = brick.copy()
            # move the brick to the right location
            # and align it with the local tangent
            t = (j + 0.5) / number_of_bricks
            p = curve.compute_point(t)
            u = curve.compute_tangent(t)
            v = cross_vectors([0.0, 0.0, 1.0], u)
            T2 = Translation(p + [0, 0, i * height])
            R = Rotation.from_basis_vectors(u, v)
            T1 = Translation(v1)
            mesh_transform(block, T2.concatenate(R).concatenate(T1))
            # add the brick to the assembly
            assembly.add_block(block)

assembly.to_json(compas_assembly.get('curvedwall.json'))

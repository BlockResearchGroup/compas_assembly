from compas.geometry import Bezier
from compas.geometry import Point, Vector, Frame, Polyline, Box
from compas.geometry import Translation
from compas.geometry import offset_polyline
from compas.geometry import intersection_line_segment_xy
from compas.utilities import linspace, pairwise, window

import compas_rhino
from compas_rhino.artists import BoxArtist


def intersection_line_polyline(line, polyline):
    for segment in pairwise(polyline.points):
        x = intersection_line_segment_xy(line, segment)
        if x:
            return Point(*x)


controlpoints = [Point(0, 0, 0), Point(3, 6, 0), Point(5, -3, 0), Point(10, 0, 0)]
controlpoly = Polyline(controlpoints)

curve = Bezier(controlpoints)
poly = Polyline(curve.locus())
poly1 = Polyline(offset_polyline(poly, +0.15))
poly2 = Polyline(offset_polyline(poly, -0.15))

points = [poly.point(t) for t in linspace(0, 1, 20)]
tangents = [(c - a).unitized() for a, b, c in window(points, 3) if a and c]
normals = [vector.cross([0, 0, 1]) for vector in tangents]
lines = [[point, point + normal] for point, normal in zip(points[1:-1], normals)]

points1 = [intersection_line_polyline(line, poly1) for line in lines]
points2 = [intersection_line_polyline(line, poly2) for line in lines]

frames = []
blocks0 = []
blocks1 = []

mpoints = []
mpoints1 = []
mpoints2 = []

for (a, b), (a1, b1), (a2, b2) in zip(pairwise(points[1:-1]), pairwise(points1), pairwise(points2)):
    p = (a + b) * 0.5
    p1 = (a1 + b1) * 0.5
    p2 = (a2 + b2) * 0.5
    t = (b - a).unitized()
    n = Vector(0, 0, 1).cross(t)
    frame = Frame(p, t, n)
    frames.append(frame)
    l1 = (b1 - a1).length
    l2 = (b2 - a2).length
    block = Box(frame, min(l1, l2) - 0.03, 0.3, 0.1)
    blocks0.append(block)
    mpoints.append(p)
    mpoints1.append(p1)
    mpoints2.append(p2)

for (a, b), (a1, b1), (a2, b2) in zip(pairwise(mpoints), pairwise(mpoints1), pairwise(mpoints2)):
    p = (a + b) * 0.5
    t = (b - a).unitized()
    n = Vector(0, 0, 1).cross(t)
    frame = Frame(p, t, n)
    frames.append(frame)
    l1 = (b1 - a1).length
    l2 = (b2 - a2).length
    block = Box(frame, min(l1, l2) - 0.03, 0.3, 0.1)
    block.transform(Translation.from_vector([0, 0, 0.1]))
    blocks1.append(block)

# ==============================================================================
# Visualization
# ==============================================================================

compas_rhino.clear_layers(["Wall::Blocks"])

for i in range(10):
    for block in blocks0:
        T = Translation.from_vector([0, 0, i * 0.2])
        artist = BoxArtist(block.transformed(T), layer="Wall::Blocks")
        artist.draw()
    for block in blocks1:
        T = Translation.from_vector([0, 0, i * 0.2])
        artist = BoxArtist(block.transformed(T), layer="Wall::Blocks")
        artist.draw()

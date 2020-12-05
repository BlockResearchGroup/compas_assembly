import os
import compas

from compas.geometry import Bezier
from compas.geometry import Point, Vector, Line, Frame, Polyline, Box, Polygon
from compas.geometry import offset_polyline
from compas.geometry import intersection_line_segment_xy
from compas.utilities import linspace, pairwise, window

from compas_plotters import GeometryPlotter


def intersection_line_polyline(line, polyline):
    for segment in pairwise(polyline.points):
        x = intersection_line_segment_xy(line, segment)
        if x:
            return Point(*x)


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'wall.json')

# ==============================================================================
# Curves
# ==============================================================================

Z = Vector(0, 0, 1)

controlpoints = [Point(0, 0, 0), Point(4, 2.5, 0), Point(6, -2.5, 0), Point(10, 0, 0)]
controlpoly = Polyline(controlpoints)

curve = Bezier(controlpoints)

poly0 = Polyline(curve.locus())
poly1 = Polyline(offset_polyline(poly0, +0.15))
poly2 = Polyline(offset_polyline(poly0, -0.15))

points0 = [poly0.point(t) for t in linspace(0, 1, 20)]
tangents0 = [(c - a).unitized() for a, b, c in window(points0, 3) if a and c]
normals0 = [Z.cross(t) for t in tangents0]

lines = [[point, point + normal] for point, normal in zip(points0[1:-1], normals0)]

points1 = [intersection_line_polyline(line, poly1) for line in lines]
points2 = [intersection_line_polyline(line, poly2) for line in lines]

# ==============================================================================
# Blocks
# ==============================================================================

frames = []
blocks = []
polygons = []

for (a, b), (a1, b1), (a2, b2) in zip(pairwise(points0[1:-1]), pairwise(points1), pairwise(points2)):
    p = (a + b) * 0.5
    t = (b - a).unitized()
    n = Z.cross(t)

    frame = Frame(p, t, n)
    frames.append(frame)

    lmin = min((b1 - a1).length, (b2 - a2).length)

    block = Box(frame, lmin - 0.03, 0.3, 0.1)

    blocks.append(block)
    polygons.append(Polygon(block.vertices[:4][::-1]))

# ==============================================================================
# Export
# ==============================================================================

compas.json_dump(blocks, FILE)

# ==============================================================================
# Visualization
# ==============================================================================

plotter = GeometryPlotter(figsize=(16, 9))

plotter.add(controlpoly, linestyle='dotted', linewidth=0.5, color=(0.5, 0.5, 0.5))
for point in controlpoints:
    plotter.add(point, edgecolor=(1.0, 0.0, 0.0))

plotter.add(poly0, color=(0.7, 0.7, 0.7), linewidth=0.5)
plotter.add(poly1, color=(0.7, 0.7, 0.7), linewidth=0.5)
plotter.add(poly2, color=(0.7, 0.7, 0.7), linewidth=0.5)

for frame in frames:
    point = frame.point
    xaxis = Line(point, point + frame.xaxis * 0.1)
    yaxis = Line(point, point + frame.yaxis * 0.1)
    plotter.add(point, edgecolor=(0, 0, 1.0), size=2)
    plotter.add(xaxis, color=(1.0, 0, 0), draw_as_segment=True)
    plotter.add(yaxis, color=(0, 1.0, 0), draw_as_segment=True)

for block in polygons:
    plotter.add(block)

plotter.zoom_extents()
plotter.show()

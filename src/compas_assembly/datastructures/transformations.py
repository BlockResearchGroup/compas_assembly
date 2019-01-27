from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import transform_points


__all__ = [
    'assembly_transform',
    'assembly_transformed'
]


def assembly_transform(assembly, T):
    """"""
    points = []
    for key in assembly.vertices():
        block = assembly.blocks[key]
        xyz = block.get_vertices_attributes('xyz')
        points.extend(xyz)
    points = transform_points(points, T)
    k = 0
    for i, (key, a) in enumerate(assembly.vertices(True)):
        block = assembly.blocks[key]
        for j, (_, b) in enumerate(block.vertices(True)):
            b['x'] = points[k][0]
            b['y'] = points[k][1]
            b['z'] = points[k][2]
            k += 1
        cx, cy, cz = block.centroid()
        a['x'] = cx
        a['y'] = cy
        a['z'] = cz


def assembly_transformed(assembly, T):
    """"""
    assembly = assembly.copy()
    assembly_transform(assembly, T)
    return assembly


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass

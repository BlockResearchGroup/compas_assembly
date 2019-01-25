from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import convex_hull_numpy
from compas.topology import unify_cycles


__all__ = ['compute_hull_numpy']


def compute_hull_numpy(assembly, keys=None):
    """"""
    keys = keys or list(assembly.vertices())

    points = []
    for key in keys:
        block = assembly.blocks[key]
        points.extend(block.get_vertices_attributes('xyz'))

    vertices, faces = convex_hull_numpy(points)

    i_index = {i: index for index, i in enumerate(vertices)}

    vertices = [points[index] for index in vertices]
    faces = [[i_index[i] for i in face] for face in faces]
    faces = unify_cycles(vertices, faces)

    return vertices, faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas_assembly
    from compas.datastructures import Mesh
    from compas.viewers import MeshViewer
    from compas_assembly.datastructures import Assembly

    assembly = Assembly.from_json(compas_assembly.get('frompolysurfaces.json'))

    vertices, faces = compute_hull_numpy(assembly)
    hull = Mesh.from_vertices_and_faces(vertices, faces)

    viewer = MeshViewer()
    viewer.mesh = hull
    viewer.show()

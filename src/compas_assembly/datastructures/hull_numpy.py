from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import convex_hull_numpy
from compas.topology import unify_cycles


__all__ = ['assembly_hull_numpy']


def assembly_hull_numpy(assembly, keys=None, unify=True):
    """Construct the convex hull of an assembly.

    Parameters
    ----------
    assembly : Assembly
        The assembly data structure.
    keys: list, optional
        The identifiers of the blocks to include in the hull calculation.
        Defaults to all blocks.
    unify : bool, optional
        Unify the face cycles of the hull.
        Default is ``True``.

    Returns
    -------
    tuple
        The vertices and faces of the hull.

    Warning
    -------
    This function requires Numpy and cannot be used directly inside Rhino.

    Examples
    --------
    .. code-block:: python

        import compas_assembly

        from compas.datastructures import Mesh
        from compas.viewers import MeshViewer

        from compas_assembly.datastructures import Assembly

        assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

        vertices, faces = assembly_hull_numpy(assembly)
        hull = Mesh.from_vertices_and_faces(vertices, faces)

        viewer = MeshViewer()
        viewer.mesh = hull
        viewer.show()

    """
    keys = keys or list(assembly.vertices())

    points = []
    for key in keys:
        block = assembly.blocks[key]
        points.extend(block.get_vertices_attributes('xyz'))

    vertices, faces = convex_hull_numpy(points)

    i_index = {i: index for index, i in enumerate(vertices)}

    vertices = [points[index] for index in vertices]
    faces = [[i_index[i] for i in face] for face in faces]

    if unify:
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

    assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

    vertices, faces = assembly_hull_numpy(assembly)
    hull = Mesh.from_vertices_and_faces(vertices, faces)

    viewer = MeshViewer()
    viewer.mesh = hull
    viewer.show()

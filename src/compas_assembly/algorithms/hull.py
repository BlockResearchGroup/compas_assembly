from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import flatten
from compas.geometry import convex_hull
from compas.topology import unify_cycles


def assembly_hull(assembly, keys=None, unify=True):
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

    Examples
    --------
    >>>

    """
    keys = keys or list(assembly.nodes())

    points = []
    for key in keys:
        block = assembly.blocks[key]
        points.extend(block.vertices_attributes('xyz'))

    faces = convex_hull(points)
    vertices = list(set(flatten(faces)))

    i_index = {i: index for index, i in enumerate(vertices)}

    vertices = [points[index] for index in vertices]
    faces = [[i_index[i] for i in face] for face in faces]

    if unify:
        faces = unify_cycles(vertices, faces)

    return vertices, faces

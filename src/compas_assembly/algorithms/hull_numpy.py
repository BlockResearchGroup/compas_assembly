from compas.geometry import convex_hull_numpy
from compas.topology import unify_cycles


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

    Warnings
    --------
    This function requires Numpy and cannot be used directly inside Rhino.

    Examples
    --------
    >>>
    """
    keys = keys or list(assembly.nodes())

    points = []
    for key in keys:
        block = assembly.blocks[key]
        points.extend(block.vertices_attributes("xyz"))

    vertices, faces = convex_hull_numpy(points)

    i_index = {i: index for index, i in enumerate(vertices)}

    vertices = [points[index] for index in vertices]
    faces = [[i_index[i] for i in face] for face in faces]

    if unify:
        faces = unify_cycles(vertices, faces)

    return vertices, faces

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import transform_points


__all__ = [
    'assembly_transform',
    'assembly_transformed'
]


def assembly_transform(assembly, T):
    """Transform an assembly by the given transformation matrix.

    Parameters
    ----------
    assembly : Assembly
        The assembly data structure.
    T : Transformation
        The transformation matrix.

    Notes
    -----
    The assembly is transformed in place. No copy is made.

    Examples
    --------
    .. code-block:: python

        assembly = Assembly.from_json('assembly.json')

        R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
        assembly_transform(assembly, R)

    """
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
    """Transform a copy of the assembly by the given transformation matrix.

    Parameters
    ----------
    assembly : Assembly
        The assembly data structure.
    T : Transformation
        The transformation matrix.

    Returns
    -------
    Assembly
        The transformed copy.

    Notes
    -----
    The assembly is transformed in place. No copy is made.

    Examples
    --------
    .. code-block:: python

        assembly = Assembly.from_json('assembly.json')

        R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
        transformed = assembly_transformed(assembly, R)

    """
    assembly = assembly.copy()
    assembly_transform(assembly, T)
    return assembly


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass

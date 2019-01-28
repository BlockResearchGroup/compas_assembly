from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from collections import deque


__all__ = [
    'assembly_block_building_sequence',
    'assembly_block_placing_frame'
]


def assembly_block_building_sequence(assembly, key):
    """Determine the sequence of blocks that need to be assembled to be able to
    place a target block.

    Parameters
    ----------
    assembly : Assembly
        An assembly data structure.
    key : hashable
        The block identifier.

    Returns
    -------
    list
        A sequence of block identifiers.

    Notes
    -----
    This will only work for properly supported *wall* assemblies of which the
    interfaces and courses have been identified.

    Examples
    --------
    .. code-block:: python

        # this code only works in Rhino

        assembly = Assembly.from_json(...)

        placed = list(assembly.vertices_where({'is_placed': True}))

        artist = AssemblyArtist(assembly, layer="Assembly")

        artist.clear_layer()
        artist.draw_vertices()
        artist.draw_blocks(show_faces=False, show_edges=True)

        if placed:
            artist.draw_blocks(keys=placed, show_faces=True, show_edges=False)

        artist.redraw()

        key = AssemblyHelper.select_vertex(assembly)

        sequence = assembly_block_building_sequence(assembly, key)

        print(sequence)

        keys = list(set(sequence) - set(placed))

        artist.draw_blocks(keys=keys, show_faces=True, show_edges=False)
        artist.redraw()

    """
    course = assembly.get_vertex_attribute(key, 'course')

    if course is None:
        raise Exception("The courses of the assembly have not been identified.")

    sequence = []
    seen = set()
    tovisit = deque([(key, course + 1)])

    while tovisit:
        k, course_above = tovisit.popleft()

        if k not in seen:
            seen.add(k)
            course = assembly.get_vertex_attribute(k, 'course')

            if course_above == course + 1:
                sequence.append(k)
                for nbr in assembly.vertex_neighbors(k):
                    if nbr not in seen:
                        tovisit.append((nbr, course))

    return sequence[::-1]


def assembly_block_placing_frame(assembly, key):
    """Compute the placing frame of a selected block.

    Parameters
    ----------
    assembly : Assembly
        An assembly data structure.
    key : hashable
        The block identifier.

    Returns
    -------
    frame
        A tuple representing a frame (origin, uvw).

    Examples
    --------
    .. code-block:: python

        pass

    """
    block = assembly.blocks[key]
    fkey = block.top()
    o, uvw = block.frame(fkey)
    o = block.face_center(fkey)
    return o, uvw


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass

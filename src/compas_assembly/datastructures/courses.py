from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__all__ = ['assembly_courses']


def assembly_courses(wall):
    """Identify the courses in a wall of blocks.

    Parameters
    ----------
    wall : Assembly
        The wall assembly data structure.

    Returns
    -------
    list of list
        The block identifiers per course.

    Examples
    --------
    >>>
    """
    courses = []
    vertices = set(wall.nodes())
    base = set(wall.nodes_where({'is_support': True}))

    if base:
        courses.append(list(base))

        seen = set()
        seen.update(base)

        vertices -= base

        while vertices:
            nbrs = set(nbr for key in courses[-1] for nbr in wall.neighbors(key))
            course = list(nbrs - seen)
            courses.append(course)
            seen.update(nbrs)
            vertices -= nbrs

    return courses


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

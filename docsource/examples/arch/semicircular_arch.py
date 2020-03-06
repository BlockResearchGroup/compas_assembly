import math
from compas.geometry import subtract_vectors
from compas.geometry import normalize_vector
from compas.geometry import angle_vectors
from compas.geometry import scale_vector
from compas.geometry import Vector
from compas.geometry import rotate_points
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import Assembly


def semicirc_arch_rise_span(h, s, d, t, n_blocks):
    """Create a semicircular arch from rise and span.

        Parameters
        ----------
        h : float
            Rise (Height) of the arch in meter measured from the impost line to the intrados
            of the keystone.
        s : float
            Dimension of the span in meter measured at the impost level (intrados-intrados).
        d : float
            Depth in meter of the arch perpendicular to the front view plane.
        t : float
            Thickness in meter of the arch.
        n_blocks: int
            number of voussoirs.

        Returns
        -------
        assembly of the semicircular arch

"""
    assembly = Assembly()

    if h > s / 2:
        print("Not a semicircular arch")
        exit()

    # radius of the arch
    radius = h / 2 + (s**2 / (8 * h))
    print('radius =', radius)

    pt0 = (0.0, 0.0, 0.0)
    pt1 = (0.0, 0.0, h)
    pt2 = (pt0[0] - s / 2, 0.0, 0.0)

    # coordinates of the circle center
    radius_pt = (pt0[0], pt0[1], pt0[2] - (radius - pt1[2]))

    # find the springing angle
    vect = normalize_vector(subtract_vectors(pt2, radius_pt))
    angle_vect = angle_vectors(vect, scale_vector(Vector.Xaxis(), -1.0))
    springing_angle = math.radians(90) - angle_vect
    print('springing_angle =', math.degrees(springing_angle))
    tot_angle = math.radians(180) - 2 * angle_vect

    a = pt1
    b = (pt1[0], pt1[1] + d, pt1[2])
    c = (pt1[0], pt1[1] + d, pt1[2] + t)
    d = (pt1[0], pt1[1], pt1[2] + t)

    # compute the angle between voussoirs
    an = tot_angle / n_blocks

    # create vossouirs
    pts = rotate_points([a, b, c, d], springing_angle, scale_vector(Vector.Yaxis(), -1.0), radius_pt)
    points = [pts]
    faces = [[0, 1, 2, 3], [0, 3, 7, 4], [0, 4, 5, 1], [5, 6, 2, 1], [6, 7, 3, 2], [5, 4, 7, 6]]

    for n in range(n_blocks + 1):
        pts1 = rotate_points([pts[0], pts[1], pts[2], pts[3]], an * n, Vector.Yaxis(), radius_pt)
        points.append(pts1)
    for n in range(n_blocks + 1):
        m = Block.from_vertices_and_faces((points[n] + points[n + 1]), faces)
        assembly.add_block(m)

    return assembly

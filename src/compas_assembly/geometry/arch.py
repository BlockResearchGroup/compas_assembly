from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import radians
from math import pi
from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import midpoint_point_point
from compas.geometry import transform_points
from compas.geometry import angle_vectors
from compas.utilities import pairwise

from compas_assembly.geometry.geometry import Geometry


__all__ = ['Arch']


# perhaps it makes more sense that parameters such as rise, span, ...
# are object attributes
# and blocks can be generated on-the-fly
# for different numbers of voussoirs (n)
# for different thicknesses
# for different ...
class Arch(Geometry):

    # def __init__(self):
    #     super(Arch, self).__init__()
    #     self.blocks = None

    @classmethod
    def from_rise_and_span(cls, rise, span, thickness, n, depth=1.0):
        """Create voussoir geometry for a semi-circular arch with given rise and span.

        Parameters
        ----------
        rise : float
            The distance between the base of the arch and the highest point of the intrados.
        span : float
            The distance between opposite intrados points at the base.
        thickness : float
            The distance between intrados and extrados.
        n : int
            Number of voussoirs
        depth : float, optional
            The depth of the arch.
            Default is ``1.0``.

        Returns
        -------
        arch : Arch
            An arch object.

        """
        if rise > span / 2:
            raise Exception("Not a semicircular arch.")

        arch = cls()

        radius = rise / 2 + span**2 / (8 * rise)

        base = [0.0, 0.0, 0.0]
        top = [0.0, 0.0, rise]
        left = [- span / 2, 0.0, 0.0]
        center = [0.0, 0.0, rise - radius]

        vector = subtract_vectors(left, center)
        springing = angle_vectors(vector, [-1.0, 0.0, 0.0])
        sector = radians(180) - 2 * springing
        angle = sector / n

        a = top
        b = add_vectors(top, [0, depth, 0])
        c = add_vectors(top, [0, depth, thickness])
        d = add_vectors(top, [0, 0, thickness])

        R = Rotation.from_axis_and_angle([0, 1.0, 0], 0.5 * sector, center)
        bottom = transform_points([a, b, c, d], R)

        blocks = []
        for i in range(n):
            R = Rotation.from_axis_and_angle([0, 1.0, 0], -angle, center)
            top = transform_points(bottom, R)
            vertices = bottom + top
            faces = [[0, 1, 2, 3], [7, 6, 5, 4], [3, 7, 4, 0], [6, 2, 1, 5], [7, 3, 2, 6], [5, 1, 0, 4]]
            block = Block.from_vertices_and_faces(vertices, faces)
            bottom = top

        arch.blocks = blocks

        return arch


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

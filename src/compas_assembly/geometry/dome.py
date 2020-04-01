from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_assembly.geometry._geometry import Geometry


__all__ = ['Dome']


# perhaps it makes more sense that parameters such as rise, span, ...
# are object attributes
# and blocks can be generated on-the-fly
# for different numbers of voussoirs (n)
# for different thicknesses
# for different ...
class Dome(Geometry):
    """Create voussoirs for a spherical dome geometry with given rise and span.

    Parameters
    ----------
    rise : float
        The distance between ...
    span : float
        The distance between ...
    thickness : float
        The distance between intrados and extrados.
    rows : int
        Number of voussoir rows.

    """

    def __init__(self, rise=None, span=None, thickness=None, rows=None):
        super(Dome, self).__init__()
        self.rise = rise
        self.span = span
        self.thickness = thickness
        self.rows = rows

    def blocks(self):
        """Compute the blocks.

        Returns
        -------
        list
            A list of blocks defined as simple meshes.

        Notes
        -----
        This method is used by the ``from_geometry`` constructor of the assembly data structure
        to create an assembly "from geometry".

        """
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

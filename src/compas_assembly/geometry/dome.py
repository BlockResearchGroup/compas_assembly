from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ._geometry import Geometry


__all__ = ['Dome']


class Dome(Geometry):
    """Create voussoirs for a spherical dome geometry with given rise and span.

    Parameters
    ----------

    """

    def __init__(self):
        super(Dome, self).__init__()

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

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_assembly.geometry._geometry import Geometry


__all__ = ['Wall']


# perhaps it makes more sense that parameters such as rise, span, ...
# are object attributes
# and blocks can be generated on-the-fly
# for different numbers of voussoirs (n)
# for different thicknesses
# for different ...
class Wall(Geometry):
    """Create voussoirs for a typical brick wall.

    Parameters
    ----------

    """

    def __init__(self):
        super(Wall, self).__init__()

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

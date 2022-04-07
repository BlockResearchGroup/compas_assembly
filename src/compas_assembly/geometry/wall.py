from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ._geometry import Geometry


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

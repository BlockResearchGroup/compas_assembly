from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

__all__ = ['Geometry']


class Geometry(object):

    __module__ = 'compas_assembly.geometry'

    def __init__(self):
        pass

    def to_blocks_and_interfaces(self):
        """Convert the geometry to a list of block meshes,
        and a list of block index pairs representing connections or interfaces.

        Returns
        -------
        tuple
            0. List of meshes representing the block geometries.
            1.
        """
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

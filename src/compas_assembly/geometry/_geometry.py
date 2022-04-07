from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class Geometry(object):
    def __init__(self):
        pass

    def blocks(self):
        raise NotImplementedError

    def interfaces(self):
        raise NotImplementedError

    def to_blocks_and_interfaces(self):
        """Convert the geometry to a list of block meshes,
        and a list of block index pairs representing connections or interfaces.

        Returns
        -------
        tuple
            0. List of meshes representing the block geometries.
            1. List of block index pairs representing connections or interfaces.
        """
        raise NotImplementedError

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_assembly.datastructures.core import Assembly as _Assembly
from compas_assembly.datastructures.transformations import assembly_transform
from compas_assembly.datastructures.transformations import assembly_transformed


__all__ = ['Assembly']


class Assembly(_Assembly):

    transform = assembly_transform
    transformed = assembly_transformed

    @classmethod
    def from_geometry(cls, geometry):
        assembly = cls()
        for block in geometry.blocks:
            assembly.add_block(block)
        return assembly


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

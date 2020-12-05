from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .core import Block
from .core import Assembly as BaseAssembly
from .transformations import assembly_transform
from .transformations import assembly_transformed


__all__ = ['Assembly']


class Assembly(BaseAssembly):

    transform = assembly_transform
    transformed = assembly_transformed

    @classmethod
    def from_geometry(cls, geometry):
        """Construct an assembly of blocks from a particular type of assembly geometry.

        Parameters
        ----------
        geometry : compas_assembly.geometry.Geometry
            A geometry object.

        Returns
        -------
        assembly : compas_assembly.datastructures.Assembly
            The resulting assembly data structure.

        """
        assembly = cls()
        for mesh in geometry.blocks():
            assembly.add_block(mesh.copy(cls=Block))
        return assembly


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

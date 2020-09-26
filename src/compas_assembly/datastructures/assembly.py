from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_assembly.datastructures.core import Block
from compas_assembly.datastructures.core import Assembly as BaseAssembly
from compas_assembly.datastructures.transformations import assembly_transform
from compas_assembly.datastructures.transformations import assembly_transformed


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
            block = mesh.copy(cls=Block)
            assembly.add_block(block)
        return assembly


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas_assembly.geometry import Arch
    from compas_assembly.datastructures import Assembly

    rise = 5
    span = 10
    depth = 0.5
    thickness = 0.7

    arch = Arch(rise, span, thickness, depth, n=40)

    arch.rise = 7
    arch.n = 20
    assembly = Assembly.from_geometry(arch)

    arch.n = 40
    assembly = Assembly.from_geometry(arch)



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

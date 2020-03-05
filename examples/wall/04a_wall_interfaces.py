"""Add a support plate to a wll assembly and identify the interfaces.

1. Load an assembly from a json file
2. Compute the footprint of the assembly
3. Add a support in the XY plane at least the size to the footprint
4. Compute the interfaces of the assembly
5. Serialise the result

"""
import os

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces_numpy


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE_I = os.path.join(DATA, 'wall_supported.json')
FILE_O = os.path.join(DATA, 'wall_interfaces.json')


# load assembly from JSON

assembly = Assembly.from_json(FILE_I)

# identify the interfaces

assembly_interfaces_numpy(assembly, nmax=100, amin=0.0001)

# serialise

assembly.to_json(FILE_O)

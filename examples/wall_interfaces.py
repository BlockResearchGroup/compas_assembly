"""Add a support plate to a wll assembly and identify the interfaces.

1. Load an assembly from a json file
2. Compute the footprint of the assembly
3. Add a support in the XY plane at least the size to the footprint
4. Compute the interfaces of the assembly
5. Serialise the result

"""
import compas_assembly
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces_numpy

FILE_I = compas_assembly.get('wall_supported.json')
FILE_O = compas_assembly.get('wall_interfaces.json')

# load assembly from JSON

assembly = Assembly.from_json(FILE_I)

# identify the interfaces

assembly_interfaces_numpy(assembly, nmax=100, amin=0.0001)

# serialise

assembly.to_json(FILE_O)

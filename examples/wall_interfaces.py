"""Add a support plate to a wll assembly and identify the interfaces.

1. Load an assembly from a json file
2. Compute the footprint of the assembly
3. Add a support in the XY plane at least the size to the footprint
4. Compute the interfaces of the assembly
5. Serialise the result

"""
import compas_assembly

from compas.geometry import bounding_box_xy
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas.geometry import centroid_points

from compas.datastructures import mesh_transform

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import assembly_interfaces_numpy


# load assembly from JSON

assembly = Assembly.from_json(compas_assembly.get('wall_courses.json'))

# identify the interfaces

assembly_interfaces_numpy(assembly, nmax=200)

# serialise

assembly.to_json(compas_assembly.get('wall_interfaces.json'))

"""Identify the courses of a assembly assembly.

1. Load an assembly from a JSON file.
2. Identify the course rows
3. serialise to JSON

Notes
-----
This will only work as expected on *wall* assemblies that are properly supported.

"""
import os

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_courses


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE_I = os.path.join(DATA, 'wall_interfaces.json')
FILE_O = os.path.join(DATA, 'wall_courses.json')


# load an assembly

assembly = Assembly.from_json(FILE_I)

# check if the assembly has supports

supports = list(assembly.nodes_where({'is_support': True}))

if not supports:
    raise Exception("The assembly has no supports.")

# identify the courses

courses = assembly_courses(assembly)

# assign course id's to the corresponding blocks

for i, course in enumerate(courses):
    assembly.nodes_attribute('course', i, keys=course)

# serialise the result

assembly.to_json(FILE_O)

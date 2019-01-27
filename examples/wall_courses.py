"""Identify the courses of a wall assembly.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces
from compas_assembly.datastructures import assembly_courses


wall = Assembly.from_json(compas_assembly.get('wall.json'))

supports = list(wall.vertices_where({'is_support': True}))

if supports:
    assembly_interfaces(wall)
    courses = assembly_courses(wall)
    print(courses)

else:
    print("The assembly has no supports.")

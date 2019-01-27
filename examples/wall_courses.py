"""Identify the courses of a assembly assembly.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_courses


assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

supports = list(assembly.vertices_where({'is_support': True}))

if supports:
    courses = assembly_courses(assembly)

    for i, course in enumerate(courses):
        assembly.set_vertices_attribute('course', i, keys=course)

    assembly.to_json(compas_assembly.get('assembly.json'))

else:
    print("The assembly has no supports.")

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

import compas
import compas_rhino
import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import identify_interfaces
from compas_assembly.datastructures import identify_courses


wall = Assembly.from_json(compas_assembly.get('frompolysurfaces.json'))

identify_interfaces(wall)

courses = identify_courses(wall)

print(courses)

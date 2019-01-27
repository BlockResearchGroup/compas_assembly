from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_interfaces
from compas_assembly.datastructures import assembly_courses


wall = Assembly.from_json(compas_assembly.get('frompolysurfaces.json'))

assembly_interfaces(wall)

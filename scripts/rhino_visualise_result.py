from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)

assembly = Assembly.from_json(os.path.join(HERE, '../data/assembly_result.json'))
assembly.draw({
    'show.vertices': True,
    'show.interfaces': True,
    'show.forces': True,
    'show.forces_as_vectors': False,
    'mode.interface': 0,
    'scale.force': 1.0
})

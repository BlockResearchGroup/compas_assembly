from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
PATH = os.path.join(DATA, 'stack.json')

assembly = Assembly.from_json(PATH)
assembly.draw({
    'layer': 'Assembly',
    'show.vertices': True,
    'show.interfaces': True,
    'show.edges': True,
    'show.forces': True,
    'show.forces_as_vectors': False,
    'mode.interface': 0,
    'scale.force': 1.0
})

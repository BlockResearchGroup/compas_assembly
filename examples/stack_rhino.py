from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas_assembly.datastructures import Assembly

FILE = compas_assembly.get('stack.json')

assembly = Assembly.from_json(FILE)
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

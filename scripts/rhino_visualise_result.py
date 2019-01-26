from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas_rhino
import compas_assembly

from compas_assembly.datastructures import Assembly

HERE = os.path.dirname(__file__)

assembly = Assembly.from_json(os.path.join(HERE, '../data/wall_result.json'))
assembly.draw({
    'show.vertices': True,
    'show.interfaces': True,
    'show.forces': True,
    'mode.interface': 0})

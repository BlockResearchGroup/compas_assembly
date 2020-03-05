"""Compute the contact forces required for static equilibrium of an assembly.

1. Make an Xfunc of ``compute_interface_forces``
2. Load an assembly from a JSON file.
3. Make a sub-assembly corresponding to the building sequence.
4. Check if the sub-assembly is properly supported.
5. Compute interface forces.
6. Visualise in Rhino.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from compas_assembly.datastructures import Assembly


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE = os.path.join(DATA, 'wall_equilibrium.json')


assembly = Assembly.from_json(FILE)

# ==============================================================================
# Visualize
# ==============================================================================

assembly.draw({
    'layer': 'Assembly',
    'show.vertices': True,
    'show.interfaces': True,
    'show.forces': True,
    'show.forces_as_vectors': False,
    'mode.interface': 0,
    'scale.force': 1.0
})

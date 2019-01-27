"""Compute the contact forces required for static equilibrium of an assembly.

1. Load an assembly from a JSON file.
2. Make sure there are supports.
3. Identify the interfaces.
4. Compute interface forces.
5. Serialise the result.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx

assembly = Assembly.from_json(compas_assembly.get('wall_support.json'))
supports = list(assembly.vertices_where({'is_support': True}))

if supports:
    compute_interface_forces_cvx(assembly, solver='CVXOPT', verbose=True)
    assembly.to_json(compas_assembly.get('wall_result.json'))

else:
    print('The wall has no supports.')

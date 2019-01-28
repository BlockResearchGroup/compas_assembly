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


# load an assembly
assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

# define a sequence of buildable blocks
sequence = [26, 21, 20, 15, 14, 9, 10, 8, 3, 4, 2, 38]

# create a sub_assembly for the sequence
sub_assembly = Assembly()

for key, attr in assembly.vertices(True):
    if key in sequence:
        block = assembly.blocks[key].copy()
        sub_assembly.add_vertex(key=key, **attr)
        sub_assembly.blocks[key] = block

for u, v, attr in assembly.edges(True):
    if u in sequence and v in sequence:
        sub_assembly.add_edge(u, v, **attr)


supports = list(sub_assembly.vertices_where({'is_support': True}))

# check if the sub_assembly is supported
if supports:

    # compute the interface forces
    compute_interface_forces_cvx(sub_assembly, solver='CVXOPT', verbose=True)

    # update the original assembly
    for u, v, attr in assembly.edges(True):
        if sub_assembly.has_edge(u, v):
            attr['interface_forces'] = sub_assembly.get_edge_attribute((u, v), 'interface_forces')
        else:
            attr['interface_forces'] = None

    # serialise to json
    assembly.to_json(compas_assembly.get('assembly.json'))

else:
    print('The assembly has no supports.')

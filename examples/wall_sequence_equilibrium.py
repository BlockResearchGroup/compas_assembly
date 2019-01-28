"""Compute the contact forces required for static equilibrium of an assembly.

1. Load an assembly from a JSON file.
2. Make sure there are supports.
3. Identify the interfaces.
4. Compute interface forces.
5. Serialise the result.

Notes
-----
the results can be visualised in Rhino with ``assembly_view_rhino.py``.
To run directly in Rhino you will need an XFunc or RPC connection.

"""
import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx


# load an assembly

assembly = Assembly.from_json(compas_assembly.get('wall_interfaces.json'))

# define a sequence of buildable blocks

sequence = [28, 22, 23, 16, 17, 18, 11, 12, 13, 5, 6, 7, 8, 0, 1, 2, 3, 38]

# create a sub_assembly for the sequence

sub = assembly.subset(sequence)

# check if the sub_assembly is supported

supports = list(sub.vertices_where({'is_support': True}))

if not supports:
    raise Exception('The sub-assembly has no supports.')

# compute the interface forces

compute_interface_forces_cvx(sub, solver='CVXOPT', verbose=True)

# update the original assembly

for u, v, attr in assembly.edges(True):
    if sub.has_edge(u, v):
        attr['interface_forces'] = sub.get_edge_attribute((u, v), 'interface_forces')
    else:
        attr['interface_forces'] = None

# serialise to json

assembly.to_json(compas_assembly.get('wall_equilibrium.json'))

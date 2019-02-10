"""Compute the contact forces required for static equilibrium of an assembly.

1. Load an assembly from a JSON file.
2. Compute interface forces.
3. Serialise the result.

"""
import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx


# load assembly

assembly = Assembly.from_json(compas_assembly.get('stack.json'))

# compute interface forces

compute_interface_forces_cvx(assembly, solver='CVXOPT', verbose=True)

# serialise

assembly.to_json(compas_assembly.get('stack.json'))

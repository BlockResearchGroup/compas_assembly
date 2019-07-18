"""Compute the contact forces required for static equilibrium of an assembly.

1. Load an assembly from a JSON file.
2. Compute interface forces.
3. Serialise the result.

"""
import os

from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'stack.json')

# load assembly

assembly = Assembly.from_json(FILE)

# compute interface forces

compute_interface_forces_cvx(assembly, solver='CVXOPT', verbose=True)

# serialise

assembly.to_json(FILE)

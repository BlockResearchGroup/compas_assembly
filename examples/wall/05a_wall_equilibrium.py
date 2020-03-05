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
import os

from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx


HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../../data')
FILE_I = os.path.join(DATA, 'wall_courses.json')
FILE_O = os.path.join(DATA, 'wall_equilibrium.json')


# load an assembly

assembly = Assembly.from_json(FILE_I)

# compute the interface forces

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)

# serialise to json

assembly.to_json(FILE_O)

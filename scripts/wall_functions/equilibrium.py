import os

from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE)
FILE_I = os.path.join(DATA, 'wall_test1_interfaces.json')
FILE_O = os.path.join(DATA, 'wall_test1_equilibrium.json')


# ==============================================================================
# Load assembly from file
# ==============================================================================

assembly = Assembly.from_json(FILE_I)

# ==============================================================================
# Interface forces
# ==============================================================================

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)

# ==============================================================================
# Export
# ==============================================================================

assembly.to_json(FILE_O)
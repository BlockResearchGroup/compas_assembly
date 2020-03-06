import os
from compas_assembly.datastructures import Assembly
from compas_rbe.equilibrium import compute_interface_forces_cvx


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE_I = os.path.join(DATA, 'arch.json')
FILE_O = os.path.join(DATA, 'arch.json')


# ==============================================================================
# Load
# ==============================================================================

assembly = Assembly.from_json(FILE_I)

# ==============================================================================
# Equilibrium
# ==============================================================================

compute_interface_forces_cvx(assembly, solver='CPLEX', verbose=True)

# ==============================================================================
# Export
# ==============================================================================

assembly.to_json(FILE_O)
import pathlib
from math import pi

# from compas_cra.equilibrium import cra_solve
import compas
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.datastructures import Assembly
from compas_assembly.geometry import Dome
from compas_assembly.viewer import DEMViewer

ASSEMBLY = pathlib.Path(__file__).parent / "dome_assembly.json"

# =============================================================================
# Template
# =============================================================================

meridians = 31
hoops = 17
oculus = pi / 20

dome = Dome(meridians=meridians, hoops=hoops, oculus=oculus)

# =============================================================================
# Assembly
# =============================================================================

assembly = Assembly.from_template(dome)

# =============================================================================
# Interfaces
# =============================================================================

assembly_interfaces(assembly, nmax=20, tmax=1e-1, amin=1e-3)

# =============================================================================
# Boundary conditions
# =============================================================================

assembly.unset_boundary_conditions()

nodes = sorted(assembly.nodes(), key=lambda node: assembly.node_point(node)[2])[:meridians]
for node in nodes:
    assembly.set_boundary_condition(node)

# =============================================================================
# Equilibrium
# =============================================================================

# CRA is too slow for this structure.
# RBE gives only an approximative result.
# Ideally, the RBE result can be used to jumpstart the CRA solver
# But this is not available yet...

# cra_solve(assembly, verbose=True)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(assembly, ASSEMBLY)

# =============================================================================
# Viz
# =============================================================================

viewer = DEMViewer()
viewer.view.camera.position = [0, -7, 4]
viewer.view.camera.look_at([0, 0, 2])

viewer.add_assembly(assembly)

viewer.run()

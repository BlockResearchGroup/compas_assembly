import pathlib

from compas_cra.equilibrium import cra_penalty_solve

import compas
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.datastructures import Assembly
from compas_assembly.geometry import Arch
from compas_assembly.viewer import DEMViewer

ASSEMBLY = pathlib.Path(__file__).parent / "arch-assembly.json"

# =============================================================================
# Arch assembly
# =============================================================================

arch = Arch(rise=3, span=10, thickness=0.3, depth=0.5, n=30)

assembly = Assembly.from_template(arch)

# =============================================================================
# Interfaces
# =============================================================================

assembly_interfaces(assembly, nmax=7, tmax=1e-3, amin=1e-2)

# =============================================================================
# Boundary conditions
# =============================================================================

assembly.unset_boundary_conditions()

nodes = sorted(assembly.nodes(), key=lambda node: assembly.node_point(node)[2])[:2]
for node in nodes:
    assembly.set_boundary_condition(node)

# =============================================================================
# Equilibrium
# =============================================================================

cra_penalty_solve(assembly)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(assembly, ASSEMBLY)

# =============================================================================
# Viz
# =============================================================================

viewer = DEMViewer()
viewer.view.camera.position = [0, -15, 3]
viewer.view.camera.look_at([0, 0, 2])

viewer.add_assembly(assembly)

viewer.run()

import pathlib

# from compas_cra.equilibrium import cra_solve
# from compas_cra.equilibrium import rbe_solve
import compas
from compas.datastructures import Mesh
from compas.geometry import Scale
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.datastructures import Assembly
from compas_assembly.viewer import DEMViewer

MESHES = pathlib.Path(__file__).parent.parent / "crossvault_blocks.json"
ASSEMBLY = pathlib.Path(__file__).parent / "crossvault-assembly.json"

# =============================================================================
# Block meshes
# =============================================================================

meshes: list[Mesh] = compas.json_load(MESHES)

for mesh in meshes:
    mesh.transform(Scale.from_factors([0.03, 0.03, 0.03]))

# =============================================================================
# Assembly
# =============================================================================

assembly = Assembly()
for mesh in meshes:
    assembly.add_block_from_mesh(mesh)

# =============================================================================
# Interfaces
# =============================================================================

assembly_interfaces(assembly, nmax=7, tmax=1e-3, amin=1e-2)

# =============================================================================
# Boundary conditions
# =============================================================================

assembly.unset_boundary_conditions()

nodes = sorted(assembly.nodes(), key=lambda node: assembly.node_point(node).z)[:4]
for node in nodes:
    assembly.set_boundary_condition(node)

# =============================================================================
# Equilibrium
# =============================================================================

# CRA is too slow for this structure.
# RBE gives only an approximative result.
# Ideally, the RBE result can be used to jumpstart the CRA solver
# But this is not available yet...

# rbe_solve(assembly)

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

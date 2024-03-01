import pathlib

import compas
import compas.datastructures  # noqa: F401
from compas.geometry import Scale
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.viewer import DEMViewer

filepath = pathlib.Path(__file__).parent / "crossvault_blocks.json"


meshes: list[compas.datastructures.Mesh] = compas.json_load(filepath)

for mesh in meshes:
    mesh.transform(Scale.from_factors([1e-2, 1e-2, 1e-2]))

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

assembly_interfaces(assembly, nmax=20, tmax=1e-3, amin=1e-2)

# =============================================================================
# Viz
# =============================================================================

viewer = DEMViewer()
viewer.add_assembly(assembly)
viewer.run()

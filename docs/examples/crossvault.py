import compas
import compas_assembly
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.viewer import DEMViewer

meshes = compas.json_load(compas_assembly.get('crossvault.json'))

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

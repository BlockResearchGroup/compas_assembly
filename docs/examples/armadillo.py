import compas
import compas_assembly
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.viewer import DEMViewer

# load meshes

meshes = compas.json_load(compas_assembly.get("armadillo.json"))

# construct assembly

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# identify interfaces

assembly_interfaces(assembly, tmax=0.02, amin=0.0001)

# ==============================================================================
# Visualization
# ==============================================================================

viewer = DEMViewer()
viewer.add_assembly(assembly)
viewer.run()

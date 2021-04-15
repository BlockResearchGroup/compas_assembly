import os
import compas

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

from compas_view2.app import App

FILE_I = os.path.join(os.path.dirname(__file__), 'armadillo_meshes.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'armadillo_assembly.json')

# ==============================================================================
# Import
# ==============================================================================

meshes = compas.json_load(FILE_I)

# ==============================================================================
# Construct assembly
# ==============================================================================

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# ==============================================================================
# Export
# ==============================================================================

compas.json_dump(assembly, FILE_O)

# ==============================================================================
# Viz
# ==============================================================================

viewer = App()

for mesh in meshes:
    viewer.add(mesh, show_faces=False, show_edges=True)

viewer.run()

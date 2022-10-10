from compas_assembly.datastructures import Assembly
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.geometry import Arch
from compas_assembly.viewer import DEMViewer

# construct an arch assembly

arch = Arch(rise=5, span=10, thickness=0.7, depth=0.5, n=40)
assembly = Assembly.from_template(arch)

# define the boundary conditions

assembly.graph.node_attribute(0, "is_support", True)
assembly.graph.node_attribute(39, "is_support", True)

# identify the interfaces

assembly_interfaces(assembly)

# ==============================================================================
# Visualisation
# ==============================================================================

viewer = DEMViewer()
viewer.add_assembly(assembly)
viewer.run()

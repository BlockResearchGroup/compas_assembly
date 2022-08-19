import os
import compas
from compas.geometry import Polygon
from compas.geometry import Scale
from compas.geometry import Pointcloud
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.algorithms import assembly_interfaces
from compas_view2.app import App
from compas_view2.objects import Collection

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, "crossvault_meshes_from_rhino.json")
FILE_O = os.path.join(HERE, "crossvault_interfaces.json")

meshes = compas.json_load(FILE_I)

# =============================================================================
# Scale
# =============================================================================

for mesh in meshes:
    mesh.transform(Scale.from_factors([1e-2, 1e-2, 1e-2]))

# =============================================================================
# Assemble
# =============================================================================

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# =============================================================================
# Interfaces
# =============================================================================

# we should make tmax dependent from the block size, as a default...
assembly_interfaces(assembly, nmax=20, tmax=1e-3, amin=1e-2)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(assembly, FILE_O)

# =============================================================================
# Viz
# =============================================================================

viewer = App()

for block in assembly.blocks():
    viewer.add(block, opacity=0.2)

points = []
for node in assembly.nodes():
    points.append(assembly.node_point(node))

viewer.add(Pointcloud(points))
# viewer.add(Collection(points), size=[20] * len(points))

interfaces = []
for edge in assembly.edges():
    for interface in assembly.edge_interfaces(edge):
        interfaces.append(Polygon(interface.points))

viewer.add(Collection(interfaces))

viewer.run()

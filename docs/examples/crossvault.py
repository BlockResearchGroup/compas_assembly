import os
import compas
from compas.geometry import Polygon
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.algorithms import assembly_interfaces
from compas_view2.app import App

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "crossvault.json")

meshes = compas.json_load(FILE)

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

# =============================================================================
# Interfaces
# =============================================================================

assembly_interfaces(assembly, nmax=20, tmax=1e-2)

# =============================================================================
# Viz
# =============================================================================

viewer = App()

for block in assembly.blocks():
    viewer.add(block, opacity=0.2)

for node in assembly.nodes():
    viewer.add(assembly.node_point(node), size=20)

for edge in assembly.edges():
    for interface in assembly.edge_interfaces(edge):
        viewer.add(Polygon(interface.points))

viewer.run()

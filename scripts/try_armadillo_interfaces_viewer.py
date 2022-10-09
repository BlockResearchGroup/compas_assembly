import os
import compas
from compas.colors import Color
from compas.geometry import Point, Line, Polygon
from compas_assembly.datastructures import Assembly
from compas_assembly.algorithms import assembly_interfaces_numpy
from compas_assembly.datastructures import Block
from compas_view2.app import App
from compas_view2.objects import Collection

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "..", "docs", "examples", "armadillo.json")

meshes = compas.json_load(FILE)

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

assembly_interfaces_numpy(assembly, tmax=0.02, amin=0.0001)

# points = []
# for node in assembly.nodes():
#     points.append(assembly.node_point(node))

# lines = []
# for edge in assembly.edges():
#     lines.append(assembly.edge_line(edge))

polygons = []
for interface in assembly.interfaces():
    polygons.append(Polygon(interface.points.tolist()))

viewer = App()
viewer.view.show_grid = False
for mesh in meshes:
    viewer.add(mesh, show_faces=False, show_edges=True, color=(0.8, 0.8, 0.8))
# viewer.add(Collection(points), color=Color.from_hex("#0092d2"))
# viewer.add(Collection(lines), color=Color.from_hex("#0092d2").lightened(50))
viewer.add(Collection(polygons), color=Color.from_hex("#0092d2"))
viewer.show()

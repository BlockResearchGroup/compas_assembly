import pathlib

from compas_cra.equilibrium import cra_solve

import compas
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import Translation
from compas_assembly.algorithms import assembly_interfaces
from compas_assembly.datastructures import Assembly
from compas_assembly.viewer import DEMViewer

HERE = pathlib.Path(__file__).parent
DATA = HERE / "wall.json"
ASSEMBLY = HERE / "wall-assembly.json"

# =============================================================================
# Import
# =============================================================================

data = compas.json_load(DATA)

params = data["params"]
curve = data["basecurve"]
course_0: list[Box] = data["courses"][0]
course_1: list[Box] = data["courses"][1]

# =============================================================================
# Courses
# =============================================================================

courses = []

for i in range(5):
    boxes = course_1 if i % 2 else course_0
    courses.append([box.transformed(Translation.from_vector([0, 0, i * box.zsize])) for box in boxes])

# =============================================================================
# Assembly
# =============================================================================

assembly = Assembly()

for course in courses:
    for box in course:
        assembly.add_block_from_mesh(Mesh.from_shape(box))

# =============================================================================
# Interfaces
# =============================================================================

assembly_interfaces(assembly, tmax=1e-6, amin=1e-2)

# =============================================================================
# Boundary conditions
# =============================================================================

assembly.unset_boundary_conditions()

nodes = sorted(assembly.nodes(), key=lambda node: assembly.node_point(node).z)
for node in nodes[: params["N"] - 1]:
    assembly.set_boundary_condition(node)

# =============================================================================
# Equilibrium
# =============================================================================

cra_solve(assembly)

# =============================================================================
# Export
# =============================================================================

compas.json_dump(assembly, ASSEMBLY)

# =============================================================================
# Viz
# =============================================================================

viewer = DEMViewer()
viewer.view.camera.position = [2, -8, 1]
viewer.view.camera.look_at([3, 0, 1])

viewer.add_assembly(assembly)

viewer.run()

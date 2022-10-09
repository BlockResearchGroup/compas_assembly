import os
import compas
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_view2.app import App

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "..", "docs", "examples", "armadillo.json")

meshes = compas.json_load(FILE)

# assembly = Assembly()
# for mesh in meshes:
#     block = mesh.copy(cls=Block)
#     assembly.add_block(block)

# Artist.clear()

# artist = Artist(assembly)
# artist.draw_blocks()
# artist.draw_selfweight(scale=5.0)

# Artist.redraw()

viewer = App()
viewer.view.show_grid = False

for mesh in meshes:
    viewer.add(mesh)

viewer.show()

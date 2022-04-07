import os
import compas
from compas.artists import Artist
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "..", "docs", "examples", "crossvault.json")

meshes = compas.json_load(FILE)

assembly = Assembly()
for mesh in meshes:
    block = mesh.copy(cls=Block)
    assembly.add_block(block)

Artist.clear()

artist = Artist(assembly)
artist.draw_blocks()
artist.draw_selfweight(scale=0.001)

Artist.redraw()

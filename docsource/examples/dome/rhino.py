import os
from math import pi
from compas_assembly.datastructures import Assembly
from compas_assembly.rhino import AssemblyArtist
from compas_rhino.artists import MeshArtist

try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE_I = os.path.join(DATA, 'dome.json')
FILE_O = os.path.join(DATA, 'dome.json')


assembly = Assembly.from_json(FILE_O)

# ==============================================================================
# Visualize
# ==============================================================================

artist = AssemblyArtist(assembly, layer="Dome")
artist.clear_layer()
# artist.draw_blocks()
# artist.draw_interfaces()
# artist.draw_resultants(scale=0.1)
# artist.color_interfaces(mode=1)
# artist.redraw()

artist = MeshArtist(None, layer="Dome::Blocks")
artist.clear_layer()

for key in assembly.nodes():
    block = assembly.blocks[key]
    artist.mesh = block
    artist.draw_faces(join_faces=True)

artist.redraw()

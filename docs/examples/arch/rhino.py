import os
from compas_assembly.datastructures import Assembly
from compas_assembly.rhino import AssemblyArtist


try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE = os.path.join(DATA, 'arch.json')


# ==============================================================================
# Load assembly from file
# ==============================================================================

assembly = Assembly.from_json(FILE)

# ==============================================================================
# Visualize
# ==============================================================================

artist = AssemblyArtist(assembly, layer="Arch")
artist.clear_layer()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_resultants(scale=0.1)
artist.color_interfaces(mode=1)
artist.redraw()

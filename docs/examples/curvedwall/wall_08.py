import os
import json
# import compas

from compas.utilities import DataDecoder

import compas_rhino
from compas_rhino.artists import BoxArtist


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'wall.json')

# ==============================================================================
# Import
# ==============================================================================

# compas.json_dump(blocks, FILE)

with open(FILE, 'r') as f:
    blocks = json.load(f, cls=DataDecoder)

# ==============================================================================
# Visualization
# ==============================================================================

compas_rhino.clear_layers(["Wall::Blocks"])

for block in blocks:
    artist = BoxArtist(block, layer="Wall::Blocks")
    artist.draw()

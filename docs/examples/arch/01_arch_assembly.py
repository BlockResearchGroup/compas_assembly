import os
from math import pi

import compas
from compas_assembly.datastructures import Assembly
from compas_assembly.geometry import Arch
from compas_assembly.rhino import AssemblyArtist


FILE = os.path.join(os.path.dirname(__file__), 'arch_assembly.json')

rise = 5
span = 10
thickness = 0.7
depth = 0.5
n = 40

arch = Arch(rise, span, thickness, depth, n)
assembly = Assembly.from_geometry(arch)

assembly.node_attribute(0, 'is_support', True)
assembly.node_attribute(n - 1, 'is_support', True)

compas.json_dump(assembly, FILE)

artist = AssemblyArtist(assembly, layer="Arch::Assembly")
artist.clear_layer()

artist.draw_nodes(color={key: (255, 0, 0) for key in assembly.nodes_where({'is_support': True})})
artist.draw_blocks()

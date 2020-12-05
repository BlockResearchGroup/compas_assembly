import os
import compas

from compas.rpc import Proxy
from compas_assembly.rhino import AssemblyArtist


proxy = Proxy('compas_assembly.datastructures')

FILE_I = os.path.join(os.path.dirname(__file__), 'crossvault_assembly.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'crossvault_interfaces.json')

assembly = compas.json_load(FILE_I)

assembly = proxy.assembly_interfaces_numpy(assembly, tmax=0.02)

compas.json_dump(assembly, FILE_O)

artist = AssemblyArtist(assembly, layer="Crossvault::Assembly")
artist.clear_layer()

artist.draw_nodes(color={key: (255, 0, 0) for key in assembly.nodes_where({'is_support': True})})
artist.draw_blocks()
artist.draw_edges()
artist.draw_interfaces()

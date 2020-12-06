import os
import compas

from compas.rpc import Proxy
from compas_assembly.rhino import AssemblyArtist


proxy = Proxy('compas_rbe.equilibrium')
proxy.restart_server()

FILE_I = os.path.join(os.path.dirname(__file__), 'arch_interfaces.json')
FILE_O = os.path.join(os.path.dirname(__file__), 'arch_equilibrium.json')

assembly = compas.json_load(FILE_I)

assembly = proxy.compute_interface_forces_cvx(assembly, solver='CPLEX')

compas.json_dump(assembly, FILE_O)

artist = AssemblyArtist(assembly, layer="Arch::Resultants")
artist.clear_layer()

artist.draw_nodes(color={key: (255, 0, 0) for key in assembly.nodes_where({'is_support': True})})
artist.draw_edges()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_resultants(scale=0.1)

import os

from compas_assembly.datastructures import Assembly
from compas_assembly.geometry import Arch
from compas_assembly.rhino import AssemblyArtist

from compas.rpc import Proxy

proxy = Proxy()
proxy.restart_server()

try:
    HERE = os.path.dirname(__file__)
except NameError:
    HERE = os.getcwd()

DATA = os.path.join(HERE, '../../../data')
FILE = os.path.join(DATA, 'arch.json')


# ==============================================================================
# Assembly
# ==============================================================================

rise = 5
span = 10
depth = 0.5
thickness = 0.7
n = 40

arch = Arch(rise, span, thickness, depth, n)
assembly = Assembly.from_geometry(arch)

assembly.node_attribute(0, 'is_support', True)
assembly.node_attribute(n - 1, 'is_support', True)

# ==============================================================================
# Identify the interfaces
# ==============================================================================

proxy.package = 'compas_assembly.datastructures'

# make proxy methods into configurable objects
# with __call__ for execution
# store the method objects in a dict of callables
assembly = proxy.assembly_interfaces_numpy(assembly, tmax=0.02)

# ==============================================================================
# Compute interface forces
# ==============================================================================

proxy.package = 'compas_rbe.equilibrium'

assembly = proxy.compute_interface_forces_cvx(assembly, solver='CPLEX')

# ==============================================================================
# Visualize
# ==============================================================================

artist = AssemblyArtist(assembly, layer="Arch")
artist.clear_layer()

artist.draw_nodes(color={key: (255, 0, 0) for key in assembly.nodes_where({'is_support': True})})
artist.draw_edges()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_resultants(scale=0.1)
# artist.color_interfaces(mode=1)

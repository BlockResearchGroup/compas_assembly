import os

from compas_assembly.datastructures import Assembly
from compas_assembly.geometry import Arch
from compas_assembly.rhino import AssemblyArtist

from compas.rpc import Proxy

proxy = Proxy()

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

data = {
    'assembly': assembly.to_data(),
    'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}}

data = proxy.assembly_interfaces_xfunc(data, tmax=0.02)

assembly.data = data['assembly']
assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}

# ==============================================================================
# Compute interface forces
# ==============================================================================

proxy.package = 'compas_rbe.equilibrium'

data = {
    'assembly': assembly.to_data(),
    'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}}

data = proxy.compute_interface_forces_xfunc(data, backend='CVX', solver='CPLEX')

assembly.data = data['assembly']
assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}

# ==============================================================================
# Visualize
# ==============================================================================

artist = AssemblyArtist(assembly, layer="Arch")
artist.clear_layer()

artist.draw_nodes(color={key: (255, 0, 0) for key in assembly.nodes_where({'is_support': True})})
artist.draw_edges()
artist.draw_blocks()
artist.draw_interfaces()
artist.draw_resultants()
artist.color_interfaces(mode=1)

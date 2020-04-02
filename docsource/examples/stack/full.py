import os
from math import pi
from random import choice
from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import scale_vector
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.plotter import AssemblyPlotter

from compas.rpc import Proxy

proxy = Proxy()


def shift(block):
    """Shift a block along the X or Y axis by a randomly chosen amount.

    Parameters
    ----------
    block : compas_assembly.datastructures.Block
    """
    scale = choice([+0.01, -0.01, +0.05, -0.05, +0.1, -0.1])
    axis = choice([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    vector = scale_vector(axis, scale)
    T = Translation(vector)
    block.transform(T)


# ==============================================================================
# Parameters
# ==============================================================================

# number of blocks

N = 10

# block dimensions

W = 2.0
H = 0.5
D = 1.0

# ==============================================================================
# Assembly
# ==============================================================================

assembly = Assembly()

# default block

box = Box.from_width_height_depth(W, H, D)
brick = Block.from_shape(box)

# make all blocks
# place each block on top of previous
# shift block randomly in XY plane

for i in range(N):
    block = brick.copy()
    block.transform(Translation([0, 0, 0.5 * H + i * H]))
    shift(block)
    assembly.add_block(block)

# mark the bottom block as support

assembly.node_attribute(0, 'is_support', True)

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

for key in assembly.edges():
    attr = assembly.edge_attributes(key)
    print(attr['interface_forces'])

# ==============================================================================
# Visualize
# ==============================================================================

R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
assembly.transform(R)

plotter = AssemblyPlotter(assembly, figsize=(8, 5), tight=True)
plotter.draw_nodes(radius=0.05)
plotter.draw_edges()
plotter.draw_blocks(facecolor={key: '#ff0000' for key in assembly.nodes_where({'is_support': True})})
plotter.show()

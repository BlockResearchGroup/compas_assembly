from math import radians
# import compas_blender
from compas.geometry import Box, Translation, Rotation
# from compas_assembly.geometry import Arch
from compas_assembly.datastructures import Block, Assembly, assembly_interfaces_numpy
# from compas_assembly.rhino import AssemblyArtist
# from compas_assembly.blender import AssemblyArtist
# from compas.rpc import Proxy

from compas_view2.app import App
from compas_view2.objects import Object, MeshObject, NetworkObject

Object.register(Block, MeshObject)
Object.register(Assembly, NetworkObject)

# proxy = Proxy('compas_assembly.datastructures')
# proxy.restart_server()

b1 = Block.from_shape(Box.from_width_height_depth(1, 1, 1))

T = Translation.from_vector([0, 0, 1])
R = Rotation.from_axis_and_angle([0, 0, 1], radians(45))

b2 = b1.transformed(T * R)

assembly = Assembly()

assembly.add_block(b1)
assembly.add_block(b2)

# arch = Arch(rise=5, span=10, thickness=0.7, depth=0.5, n=40)
# assembly = Assembly.from_geometry(arch)

assembly_interfaces_numpy(assembly)

# # artist = AssemblyArtist(assembly, layer='Assembly')
# # artist.clear_layer()

# # artist.draw_nodes()
# # artist.draw_edges()
# # artist.draw_blocks(show_faces=False)
# # artist.draw_interfaces()

# compas_blender.clear()

# artist = AssemblyArtist(assembly)
# artist.clear_layer()

# artist.draw_blocks(show_faces=False)
# artist.draw_interfaces()
# artist.draw_nodes()
# artist.draw_edges()

viewer = App()
viewer.add(assembly)
for node in assembly.nodes():
    block = assembly.node_attribute(node, 'block')
    viewer.add(block)
viewer.show()

import os
import compas
from compas.artists import Artist
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas.rpc import Proxy

proxy = Proxy("compas_assembly.algorithms")
# proxy.restart_server()

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "..", "data", "curvedwall.json")
FILE = "/Users/vanmelet/Desktop/Assembly.json"

# data = compas.json_load(FILE)

# assembly = Assembly()
# for key in data["assembly"]["vertex"]:
#     block = Block.from_data(data["blocks"][key])
#     node = int(key)
#     attr = data["assembly"]["vertex"][key]
#     assembly.add_block(block, node=node, attr_dict=attr)

assembly = Assembly.from_json(FILE)

assembly = proxy.assembly_interfaces_numpy(assembly, tmax=0.1, nmax=100)

Artist.clear()

artist = Artist(assembly)
# artist.draw_nodes()
# artist.draw_edges()
artist.draw_blocks(show_faces=False, show_edges=True)
artist.draw_interfaces(show_frames=False)
artist.draw_selfweight(scale=0.1)

Artist.redraw()

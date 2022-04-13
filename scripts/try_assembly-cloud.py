import os
import compas
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_cloud import Proxy

proxy = Proxy()
proxy.cloud_start()

assembly_interfaces = proxy.function(
    "compas_assembly.algorithms.assembly_interfaces_numpy"
)

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "..", "data", "curvedwall.json")

data = compas.json_load(FILE)

assembly = Assembly()
for key in data["assembly"]["vertex"]:
    block = Block.from_data(data["blocks"][key])
    node = int(key)
    attr = data["assembly"]["vertex"][key]
    assembly.add_block(block, node=node, attr_dict=attr)

assembly = assembly_interfaces(assembly)
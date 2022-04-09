import os
import compas
from compas.artists import Artist
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.algorithms import assembly_interfaces_numpy

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, "..", "data", "ursula.json")

# data = compas.json_load(FILE)

# assembly = Assembly()
# for key in data["assembly"]["vertex"]:
#     block = Block.from_data(data["blocks"][key])
#     node = int(key)
#     attr = data["assembly"]["vertex"][key]
#     assembly.add_block(block, node=node, attr_dict=attr)

assembly = Assembly.from_json(FILE)

assembly = assembly_interfaces_numpy(assembly)

assembly.to_json(FILE)
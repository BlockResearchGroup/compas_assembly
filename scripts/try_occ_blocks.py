import os
import compas
from compas_occ.brep import BRep, BRepFace, BRepLoop, BRepEdge

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, "fromrhino.json")
FILE_O = os.path.join(HERE, "armadillo_breps.json")

fromrhino = compas.json_load(FILE_I)

# weird = [79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 328, 329, 330, 331]

blocks = []
for i, blockdata in enumerate(fromrhino):
    faces = []
    for j, facedata in enumerate(blockdata):
        edges = []
        for curve in facedata["loop"]:
            edge = BRepEdge.from_curve(curve)
            edges.append(edge)
        loop = BRepLoop.from_edges(edges)
        surface = facedata["surface"]
        # if j == 0 and i not in weird:
        #     loop.occ_wire.Reverse()
        face = BRepFace.from_surface(surface, loop=loop)
        faces.append(face)
    block = BRep.from_faces(faces)
    blocks.append(block)

compas.json_dump(blocks, FILE_O)

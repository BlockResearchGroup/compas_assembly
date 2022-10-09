import os
import compas
import compas_rhino
from compas_rhino.geometry import RhinoNurbsCurve
from compas_rhino.geometry import RhinoNurbsSurface

FILE = os.path.join(os.path.dirname(__file__), "fromrhino.json")

blocks = []

guids = compas_rhino.select_surfaces()
objects = [compas_rhino.find_object(guid) for guid in guids]

for obj in objects:
    faces = []
    for face in obj.BrepGeometry.Faces:
        loop = face.OuterLoop
        curve = loop.To3dCurve()
        segments = curve.Explode()
        surface = obj.BrepGeometry.Surfaces[face.SurfaceIndex].ToNurbsSurface()
        faces.append(
            {
                "loop": [RhinoNurbsCurve.from_rhino(segment) for segment in segments],
                "surface": RhinoNurbsSurface.from_rhino(surface),
            }
        )
    blocks.append(faces)

compas.json_dump(blocks, FILE)

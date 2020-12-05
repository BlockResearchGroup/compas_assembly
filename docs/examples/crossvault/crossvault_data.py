import os

import compas
import compas_rhino
from compas_rhino.geometry import RhinoSurface
from compas_rhino.artists import MeshArtist


def filterfunc(face):
    success, w, h = face.GetSurfaceSize()
    if success:
        if w > 10 and h > 10:
            return True
    return False


FILE = os.path.join(os.path.dirname(__file__), 'crossvault.json')

guids = []
for guid in compas_rhino.select_surfaces():
    if compas_rhino.rs.IsPolysurface(guid):
        guids.append(guid)

meshes = []
for guid in guids:
    surf = RhinoSurface.from_guid(guid)
    mesh = surf.to_compas(facefilter=filterfunc)
    meshes.append(mesh)

compas.json_dump(meshes, FILE)

for mesh in meshes:
    artist = MeshArtist(mesh)
    artist.draw()

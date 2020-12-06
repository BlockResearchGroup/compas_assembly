import os

import compas
import compas_rhino
from compas_rhino.geometry import RhinoSurface
from compas_rhino.artists import MeshArtist


def filterfunc(face):
    return True


FILE = os.path.join(os.path.dirname(__file__), 'armadillo_meshes.json')

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

compas_rhino.clear_layers(['Armadillo'])

for mesh in meshes:
    artist = MeshArtist(mesh, layer="Armadillo::Meshes")
    artist.draw()

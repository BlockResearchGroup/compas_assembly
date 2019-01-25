from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

import compas
import compas_rhino
import compas_assembly

from compas.datastructures import Mesh
from compas.viewers import MeshViewer
from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import compute_hull_numpy


wall = Assembly.from_json(compas_assembly.get('frompolysurfaces.json'))

vertices, faces = compute_hull_numpy(wall)

hull = Mesh.from_vertices_and_faces(vertices, faces)

viewer = MeshViewer()
viewer.mesh = hull
viewer.show()
